#  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
#  NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
#  property and proprietary rights in and to this material, related
#  documentation and any modifications thereto. Any use, reproduction,
#  disclosure or distribution of this material and related documentation
#  without an express license agreement from NVIDIA CORPORATION or
#  its affiliates is strictly prohibited.
"""Helper methods for Invoke tasks."""

import os
from pathlib import Path
import re
from typing import Any

from invoke import Context
from invoke.exceptions import Exit
from invoke.runners import Result
import dotenv


def load_dotenv() -> None:
    """Load environment variables from the development configs."""
    dotenv.load_dotenv("./development/development.env")
    dotenv.load_dotenv("./development/creds.env")


def get_docker_nautobot_version(context: Context) -> str:
    """Extract the Nautobot version installed in the base Docker image."""
    nautobot_ver = context.nautobot_fsus.nautobot_ver
    python_ver = context.nautobot_fsus.python_ver

    dockerfile_path = os.path.join(context.nautobot_fsus.compose_dir, "Dockerfile")
    base_image = context.run(
        f"grep --max-count=1 '^FROM ' {dockerfile_path}",
        hide=True
    ).stdout.strip().split(" ")[1]
    base_image = base_image.replace(
        r"${NAUTOBOT_VER}",
        nautobot_ver
    ).replace(r"${PYTHON_VER}", python_ver)
    pip_nautobot_ver = context.run(
        f"docker run --rm --entrypoint '' {base_image} pip show nautobot",
        hide=True
    )
    match_version = re.search(
        r"^Version: (.*)$",
        pip_nautobot_ver.stdout.strip(),
        flags=re.MULTILINE,
    )
    if match_version:
        return match_version.group(1)
    else:
        raise Exit(f"Could not extract Nautobot version from Docker base image {base_image}.")


def is_truthy(arg: bool | str | int) -> bool:
    """
    Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1;
            false values are n, no, f, false, off and 0.
            Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False

    raise ValueError(f"Invalid truth value {arg}")


def docker_compose(context: Context, command: str, **kwargs: Any) -> Result:
    """
    docker-compose helper function.

    Helper function for running a specific docker-compose command with all
    appropriate parameters and environment.

    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker-compose ..."
            command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        # Note: 'docker-compose logs' will stop following after 60 seconds by default,
        # so we are overriding that by setting this environment variable.
        "COMPOSE_HTTP_TIMEOUT": context.nautobot_fsus.compose_http_timeout,
        "NAUTOBOT_VER": context.nautobot_fsus.nautobot_ver,
        "PYTHON_VER": context.nautobot_fsus.python_ver,
    }
    if env_vars := kwargs.pop("env", {}):
        build_env.update(env_vars)

    compose_command = [
        "docker compose",
        f"--project-name {context.nautobot_fsus.project_name}",
        f"--project-directory {context.nautobot_fsus.compose_dir}",
    ]

    compose_dir = Path(context.nautobot_fsus.compose_dir)
    for compose_file in context.nautobot_fsus.compose_files:
        compose_file_path = os.path.join(compose_dir, compose_file)
        compose_command.append(f"-f {compose_file_path}")

    compose_command.append(command)

    print(f'Running docker-compose command "{command}"')
    return context.run(" ".join(compose_command), env=build_env, **kwargs)


def run_command(context: Context, command: str, service: str = "nautobot",
                pty: bool = True, **kwargs: Any) -> None:
    """Wrapper to run a command locally or inside the nautobot container."""
    if is_truthy(context.nautobot_fsus.local):
        context.run(command, **kwargs)
    else:
        # Check if nautobot is running, no need to start another nautobot container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if service in results.stdout:
            build_command = ["exec"]
            if setenv := kwargs.get("env", {}):
                for env_var in setenv:
                    build_command.append(f"-e {env_var}")

            build_command.extend([service, command])
            compose_command = " ".join(build_command)
        else:
            compose_command = f"run --entrypoint '{command}' {service}"

        docker_compose(context, compose_command, pty=pty, **kwargs)
