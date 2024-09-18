#  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
#  NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
#  property and proprietary rights in and to this material, related
#  documentation and any modifications thereto. Any use, reproduction,
#  disclosure or distribution of this material and related documentation
#  without an express license agreement from NVIDIA CORPORATION or
#  its affiliates is strictly prohibited.
"""Cluster control tasks."""
import os

from invoke import Context, task

from tasks import helpers


@task(name="help")
def help_task(context: Context) -> None:
    """Show the help messages for all configured tasks."""
    from tasks import namespace
    for task_name in namespace.task_names:
        print(50 * "-")
        print(f"invoke {task_name} --help")
        context.run(f"invoke {task_name} --help")


# =================================================================== #
# Build
# =================================================================== #
@task(
    help={
        "force-rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    },
)
def build(context: Context, force_rm: bool = False, cache: bool = True) -> None:
    """Build the Nautobot docker image with the plugin installed."""
    command = ["build"]

    if force_rm is True:
        command.append("--force-rm")
    if cache is False:
        command.append("--no-cache")

    print(f"Building Nautobot with python {context.nautobot_fsus.python_ver}")
    helpers.docker_compose(context, " ".join(command))


@task
def generate_packages(context: Context) -> None:
    """Generate all python packages inside a docker container and copy them to ./dist"""
    helpers.run_command(context, "poetry build")


@task
def lock(context: Context) -> None:
    """Generate the poetry.lock file in the Nautobot container"""
    helpers.run_command(context, "poetry lock --no-update")


# =================================================================== #
# Service Control
# =================================================================== #
@task
def debug(context: Context) -> None:
    """Start Nautobot and/or its dependencies in debug mode."""
    print("Starting virtual cluster in debug mode...")
    helpers.docker_compose(context, "up")


@task
def start(context: Context) -> None:
    """Start Nautobot and/or its dependencies in detached mode."""
    print("Starting virtual cluster in detached mode...")
    helpers.docker_compose(context, "up --detach")


@task
def restart(context: Context) -> None:
    """Restart the virtual cluster."""
    print("Restarting virtual cluster...")
    helpers.docker_compose(context, "restart")


@task
def stop(context: Context) -> None:
    """Stop Nautobot and/or its dependencies."""
    print("Stopping virtual cluster...")
    helpers.docker_compose(context, "down")


@task
def destroy(context: Context) -> None:
    """Destroy containers and volumes for Nautobot and/or its dependencies."""
    print("Destroying virtual cluster...")
    helpers.docker_compose(context, "down --volumes")


@task
def export(context: Context) -> None:
    """Export docker compose configuration to `compose.yaml` file.

    Useful to:

    - Debug docker compose configuration.
    - Allow using `docker compose` command directly without invoke.
    """
    helpers.docker_compose(context, "convert > compose.yaml")


@task(
    help={
        "service": "docker-compose service name to view (default: nautobot).",
        "follow": "Follow the logs.",
        "tail": "Tail N number of lines, or `all`.",
    },
)
def logs(context: Context, service: str = "nautobot", follow: bool = False,
         tail: str | None = None) -> None:
    """View the logs of a docker-compose service."""
    command = ["logs"]

    if follow is True:
        command.append("--follow")
    if tail is not None:
        command.append(f"--tail={tail}")

    command.append(service)

    helpers.docker_compose(context, " ".join(command))


# =================================================================== #
# Actions
# =================================================================== #
@task
def nbshell(context: Context) -> None:
    """Launch an interactive nbshell session."""
    helpers.run_command(context, "nautobot-server nbshell")


@task
def shell_plus(context: Context) -> None:
    """Launch an interactive shell_plus session."""
    helpers.run_command(context, "nautobot-server shell_plus")


@task
def cli(context: Context) -> None:
    """Launch a bash shell inside the running Nautobot container."""
    helpers.run_command(context, "bash")


@task(
    help={
        "service": "Docker compose service name to run command in (default: nautobot).",
        "command": "Command to run (default: bash).",
        "file": "File to run command with (default: empty)",
    },
)
def exec(context: Context, service: str = "nautobot", command: str = "bash", file: str = "") -> None:
    """Run a command inside a container (defaults to bash shell inside nautobot container)."""
    command = [command, f"< '{file}'" if file else ""]
    helpers.run_command(context, " ".join(command), service=service, pty=not bool(file))


@task(
    help={
        "query": "SQL command to execute and quit (default: empty)",
        "input": "SQL file to execute and quit (default: empty)",
        "output": "Ouput file, overwrite if exists (default: empty)",
    }
)
def dbshell(context: Context, query: str = "", input: str = "", output: str = "") -> None:
    """
    Start database client inside the running `db` container.

    Determines which database backend is configured and launches the appropriate client.
    """
    if input and query:
        raise ValueError("Cannot specify both, `input` and `query` arguments")
    if output and not (input or query):
        raise ValueError("`output` argument requires `input` or `query` argument")

    helpers.load_dotenv()

    env_vars = {}
    command = []

    if "docker-compose.mysql.yml" in context.nautobot_fsus.compose_files:
        env_vars["MYSQL_PWD"] = os.getenv("MYSQL_PASSWORD")
        command.extend([
            "mysql",
            f"--user='{os.getenv('MYSQL_USER')}'",
            f"--database='{os.getenv('MYSQL_DATABASE')}'",
        ])
        if query:
            command.append(f"--'query={query}'")
    elif "docker-compose.postgres.yml" in context.nautobot_fsus.compose_files:
        command.extend([
            "psql",
            f"--username='{os.getenv('POSTGRES_USER')}'",
            f"--dbname='{os.getenv('POSTGRES_DB')}'",
        ])
        if query:
            command.append(f"--command='{query}'")
    else:
        raise ValueError("Unsupported database backend.")

    if input:
        command.append(f"< '{input}'")
    if output:
        command.append(f"> '{output}'")

    helpers.run_command(
        context,
        " ".join(command),
        service="db",
        pty=not (input or output or query),
        env=env_vars,
    )


@task(
    help={
        "input": "SQL dump file to import into the database and replace all current data. "
                 "This can be generated using `invoke backup-db`. Default is 'dump.sql'.",
    }
)
def import_db(context: Context, input: str = "dump.sql") -> None:
    """
    Stop the Nautobot containers and import a database dump file.

    Replaces all current data in the `db` container with the contents of the `input` file.
    """
    helpers.docker_compose(context, "stop -- nautobot worker")

    helpers.load_dotenv()

    env_vars = {}
    command = []

    if "docker-compose.mysql.yml" in context.nautobot_fsus.compose_files:
        env_vars["MYSQL_PWD"] = os.getenv("MYSQL_PASSWORD")
        command.extend([
            "mysql",
            f"--user='{os.getenv('MYSQL_USER')}'",
            f"--database='{os.getenv('MYSQL_DATABASE')}'",
        ])
    elif "docker-compose.postgres.yml" in context.nautobot_fsus.compose_files:
        command.extend([
            "psql",
            f"--username='{os.getenv('POSTGRES_USER')}'",
            "postgres",
        ])
    else:
        raise ValueError("Unsupported database backend.")

    command.append(f"< '{input}'")

    helpers.run_command(context, " ".join(command), service="db", pty=False, env=env_vars)

    print("Database import complete, you can start Nautobot now: `invoke start`")


@task(
    help={
        "output": "Output file for the database dump, default is 'dump.sql'. Will be "
                  "overwritten if it exists.",
        "readable": "Format the database dump in a more readable format, default is True",
    }
)
def backup_db(context: Context, output: str = "dump.sql", readable: bool = True) -> None:
    """Create a new database dump file from the running `db` container."""
    helpers.load_dotenv()

    env_vars = {}
    command = []

    if "docker-compose.mysql.yml" in context.nautobot_fsus.compose_files:
        env_vars["MYSQL_PWD"] = os.getenv("MYSQL_ROOT_PASSWORD")
        command.extend([
            "mysqldump",
            "--user=root",
            "--add-drop-database",
            "--skip-extended-insert" if readable else "",
            "--databases",
            os.getenv("MYSQL_DATABASE", ""),
        ])
    elif "docker-compose.postgres.yml" in context.nautobot_fsus.compose_files:
        command.extend([
            "pg_dump",
            "--clean",
            "--create",
            "--if-exists",
            f"--username='{os.getenv('POSTGRES_USER')}'",
            f"--dbname='{os.getenv('POSTGRES_DB')}'",
        ])
        if readable:
            command.append("--inserts")
    else:
        raise ValueError("Unsupported database backend.")

    if output:
        command.append(f"> '{output}'")

    helpers.run_command(context, " ".join(command), service="db", pty=False, env=env_vars)

    print(50 * "=")
    print("Database backup completed successfully.")
    if output:
        print(f"Dump file: {output}")
        print("To restore the database from this backup, run:")
        print(f"invoke import-db --input {output}")
    print(50 * "=")


@task(
    help={
        "user": "Username of the superuser to create (default: 'admin')",
    },
)
def createsuperuser(context: Context, user: str = "admin") -> None:
    """Create a new Nautobot superuser account (default: "admin"), will prompt for password."""
    helpers.run_command(context, f"nautobot-server createsuperuser --username {user}")


@task(
    help={
        "name": "Name for the created migration, will be auto-generated if unspecified.",
    },
)
def makemigrations(context: Context, name: str | None = None) -> None:
    """Perform the Django `makemigrations` operation."""
    command = ["nautobot-server", "makemigrations", context.nautobot_fsus.project_source]

    if name is not None:
        command.extend(["--name", name])

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "plan": "List all migrations in the order they will be applied.",
        "verbose": "Verbose output. When showing the default list, this will include the "
                   "dates and times the migrations were applied. When showing the plan list, "
                   "all direct and reverse dependencies will be included."
    }
)
def showmigrations(context: Context, plan: bool = False, verbose: bool = False) -> None:
    """Show the list of all applied migrations."""
    command = ["nautobot-server", "showmigrations"]

    if plan:
        command.append("-p")

    if verbose:
        command.append("-v2")

    helpers.run_command(context, " ".join(command))


@task
def migrate(context) -> None:
    """Perform the Django migrate operation."""
    helpers.run_command(context, "nautobot-server migrate")


@task
def post_upgrade(context: Context) -> None:
    """
    Performs common Nautobot post-upgrade operations using a single entrypoint.

    This will run the following management commands with default settings, in order:

    - migrate
    - trace_paths
    - collectstatic
    - remove_stale_contenttypes
    - clearsessions
    - invalidate all
    """
    helpers.run_command(context, "nautobot-server post_upgrade")


@task
def create_env(context: Context) -> None:
    """Add a base set of data to Nautobot to make development easier."""
    helpers.run_command(context, "nautobot-server create_fsus_env --with-fsus")

@task(
    help={
        "local": "Force the command to run locally instead of in the service container."
    }
)
def mkdocs(context: Context, local: bool = False) -> None:
    """Runs `mkdocs` to create the static documentation for the plugin."""
    command = ["mkdocs build --no-directory-urls --strict"]
    if local:
        context = context
        context.nautobot_fsus.local = True
        command.insert(0, "poetry run")

    helpers.run_command(context, " ".join(command))
