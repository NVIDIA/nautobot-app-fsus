#  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
#  NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
#  property and proprietary rights in and to this material, related
#  documentation and any modifications thereto. Any use, reproduction,
#  disclosure or distribution of this material and related documentation
#  without an express license agreement from NVIDIA CORPORATION or
#  its affiliates is strictly prohibited.
"""Task definitions for Invoke."""
import os
from pathlib import Path

from invoke import Collection
import toml

from tasks import control
from tasks import test

BASE_DIR = Path(os.path.dirname(__file__)).parent


def _required_nautobot_version() -> str:
    """Check the plugin package metadata for the required Nautobot version."""
    pyproject = toml.load("pyproject.toml")
    metadata = pyproject.get("tool", {}).get("poetry", {})

    # Get the nautobot version from pyproject.toml. It should be [tool.poetry.dependencies],
    # but if it's not there, try [tool.poetry.group.localdev.dependencies], and finally
    # return "latest" as the default if neither path is set.
    version = metadata["dependencies"].get(
        "nautobot",
        metadata.get("group", {}).get("localdev", {}).get("dependencies", {}).get(
            "nautobot",
            "stable",
        )
    )

    # The nautobot version dependency should be specified with a leading ^ for safety, so
    # that if the environment deploy image is updated to a newer version of nautobot, the
    # plugin dependency doesn't step on that and downgrade the version in the image.
    return version.lstrip("^~")


# Create the namespace here and load the tasks from a module
# to simplify getting them all into the namespace.
namespace: Collection = Collection.from_module(control)
namespace.add_collection(Collection.from_module(test))
namespace.configure(
    {
        "nautobot_fsus": {
            "nautobot_ver": _required_nautobot_version(),
            "project_name": "nautobot-fsus",
            "project_source": "nautobot_fsus",
            "python_ver": "3.10",
            "local": False,
            "compose_dir": BASE_DIR.joinpath("development").as_posix(),
            "compose_files": [
                "docker-compose.base.yml",
                "docker-compose.redis.yml",
                "docker-compose.postgres.yml",
                "docker-compose.dev.yml",
            ],
            "compose_http_timeout": "86400",
        },
        "base_dir": BASE_DIR.as_posix(),
    }
)
