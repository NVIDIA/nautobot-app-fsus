# Building Your Development Environment

## Quickstart Guide

The development environment can be used in two ways:

1. **(Recommended)** All services, including Nautobot, are spun up using [Docker and a local mount](#docker-development-environment) - the plugin source code is mounted in the service docker container so that you may continue to develop locally, and your changes will be reflected in the running container automatically.
2. With a [local Poetry environment](#local-development-environment) if you wish to develop outside of Docker, with the caveat that external services for the database (PostgreSQL by default, MySQL optionally) and Redis will be provided via Docker.

### Prerequisites

!!! note
    These are required no matter which development environment you choose.

1. Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2. Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.
3. Create your poetry python virtual environment, including the `invoke` tool.
!!! note
    ```
    ➜ poetry env use python3.10
    ➜ poetry install
    ```
4. Copy `development/creds.example.env` to `development/creds.env` (this file will be ignored by Git and Docker).
5. Copy `invoke.example.yml` to `invoke.yml` (also ignored by Git), and edit it as necessary.
!!! note
    To use MySQL as your database backend, copy `invoke.mysql.yml` to `invoke.yml` instead.

!!! tip
    Poetry can be use either with its shell (aka virtualenv) activated, or as a wrapper command.
    With the shell activated, your prompt will change to indicate the environment, and you can use all modules and commands installed in the poetry environment directly.
    ```
    ➜ poetry shell
    (nautobot-fsus-py3.10)➜ invoke start
    ...
    (nautobot-fsus-py3.10)➜ invoke test.everything -k
    ```
    Alternatively, you can preface commands installed in the poetry environment with `poetry run`.
    ```
    ➜ poetry run invoke start
    ...
    ➜ poetry run invoke test.everything -k
    ```

### Invoke

The [Invoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment.
There are a few configuration parameters which can be passed to Invoke to override the default configuration:

- `nautobot_ver`: the version of Nautobot to use as a base for any built docker containers.
- `project_name`: the default docker compose project name (default: `nautobot_fsus`).
- `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.10).
- `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers).
- `compose_dir`: the full path to a directory containing the project compose files.
- `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information).

Using **Invoke** these configuration options can be overridden using [several methods](https://docs.pyinvoke.org/en/stable/concepts/configuration.html). Perhaps the simplest is setting an environment variable `INVOKE_NAUTOBOT_CONSUMABLES_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override.
The only exception is `compose_files`, because it is a list it must be overridden in a YAML file.
There is an example `invoke.yml` (`invoke.example.yml`) in this directory which can be used as a starting point.

## Docker Development Environment

!!! tip
    This is the recommended option for development.

Once the [prerequisite steps](#prerequisites) have been completed, build and start the development server:
```shell
➜ poetry shell
➜ poetry install
➜ invoke build
➜ invoke start
```

The Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080), and the live documentation at [http://localhost:8001](http://localhost:8001)

To either stop or destroy the development environment use the following options.

`invoke stop`
:    Stop the containers, but keep all underlying systems intact

`invoke destroy`
:    Stop and remove all containers, volumes, etc. (This results in data loss due to the volume being deleted)

With the environment up, you should see five running Docker containers:
```shell
➜ docker ps

CONTAINER ID   IMAGE                                         COMMAND                  CREATED          STATUS                    PORTS                    NAMES
acc98ecb33bb   nautobot-fsus/nautobot:1.6.25-py3.10          "sh -c 'nautobot-ser…"   56 seconds ago   Up 44 seconds (healthy)   8080/tcp                 nautobot-fsus-worker-1
760cb8d52eb0   nautobot-fsus/nautobot:1.6.25-py3.10          "/docker-entrypoint.…"   56 seconds ago   Up 44 seconds (healthy)   0.0.0.0:8080->8080/tcp   nautobot-fsus-nautobot-1
045232a98222   nautobot-fsus/nautobot:1.6.25-py3.10          "mkdocs serve -v -a …"   56 seconds ago   Up 55 seconds             0.0.0.0:8001->8080/tcp   nautobot-fsus-docs-1
d2e6933582d2   postgres:14-alpine                            "docker-entrypoint.s…"   56 seconds ago   Up 55 seconds (healthy)   5432/tcp                 nautobot-fsus-db-1
585ba6cf6197   redis:6-alpine                                "docker-entrypoint.s…"   56 seconds ago   Up 55 seconds             6379/tcp                 nautobot-fsus-redis-1
```

### Real-Time Updates? How Cool!

Your environment should now be fully setup, all necessary Docker containers are created and running, and you're logged into Nautobot in your web browser.
Now what?

Now you can start developing your Nautobot app in the project folder!

The magic here is the root directory is mounted inside your Docker containers when built and ran, so **any** changes made to the files in here are directly updated to the Nautobot app code running in Docker.
This means that as you modify the code in your Nautobot app folder, the changes will be instantly updated in Nautobot.

!!! warning
	There are a few exceptions to this, as outlined in the section [To Rebuild or Not To Rebuild](#to-rebuild-or-not-to-rebuild).

The back-end Django process is setup to automatically reload itself (it only takes a couple of seconds) every time a file is updated (saved).
So for example, if you were to update one of the files like `tables.py`, then save it, the changes will be visible right away in the web browser!

!!! note
	You may get connection refused while Django reloads, but it should be refreshed fairly quickly.

### Docker Logs

When trying to debug an issue, one helpful thing you can look at are the logs within the Docker containers.

```bash
➜ invoke logs -f
```

!!! note
	The `-f` tag will keep the logs open, and output them in realtime as they are generated.
    By default this will show the logs from the `nautobot` container, to view the logs from a different container use the `-s` option with the container's service name, e.g. `invoke logs -f -s db`.

## Local Development Environment

1. Uncomment the `NAUTOBOT_DB_HOST`, `NAUTOBOT_REDIS_HOST`, and `NAUTOBOT_CONFIG` variables in `development/creds.env`.
2. Create an `invoke.yml` file with the following contents at the root of the repo and edit as necessary - e.g. set `compose_files` to `docker-compose-requirements-mysql.yml` to use MySQL as the database backend.
    ```yaml
    ---
    nautobot_fsus:
      local: true
      compose_dir: "development"
      compose_files:
        - "docker-compose.requirements.yml"
    ```
3. Install the local development dependencies and start the supporting services.
    ```shell
    ➜ poetry shell
    ➜ poetry install
    ➜ export $(cat development/dev.env | grep -v '^#' | xargs)
    ➜ export $(cat development/creds.env | grep -v '^#' | xargs)
    ➜ invoke start && sleep 5
    ➜ nautobot-server migrate
    ```
    !!! tip
        If you want to develop on the latest develop branch of Nautobot, run the following command: `poetry add --optional git+https://github.com/nautobot/nautobot@develop`. After the `@` symbol must match either a branch or a tag.
4. You can now run nautobot-server commands as you would from the [Nautobot documentation](https://nautobot.readthedocs.io/en/latest/) for example to start the development server:
    ```shell
    ➜ nautobot-server runserver 0.0.0.0:8080 --insecure
    ```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

It is typically recommended to launch the Nautobot `runserver` command in a separate shell so you can keep developing and manage the webserver separately.

With the environment up, you should see three running Docker containers:
```shell
➜ docker ps

CONTAINER ID   IMAGE                              COMMAND                  CREATED         STATUS                            PORTS                    NAMES
9a3ef787dae6   postgres:14-alpine                 "docker-entrypoint.s…"   9 seconds ago   Up 8 seconds (health: starting)   0.0.0.0:5432->5432/tcp   nautobot-fsus-postgres-1
4b435ababbab   redis:6-alpine                     "docker-entrypoint.s…"   9 seconds ago   Up 8 seconds                      0.0.0.0:6379->6379/tcp   nautobot-fsus-redis-1
```

## Updating the Documentation

Documentation dependencies are pinned to exact versions to ensure consistent results.
For the development environment, they are defined in the `pyproject.toml` file.

If you need to update any of the documentation dependencies to a newer version, make sure you copy the exact same versions pinned in `pyproject.toml` to the `docs/requirements.txt` file as well.
The latter is used in the automated build pipeline on ReadTheDocs to build the live version of the documentation.

## CLI Helper Commands

CLI helper commands are all based on [Invoke](https://www.pyinvoke.org/), and are listed below in 3 categories:

- Environment Management
- Utility
- Testing

!!! tip
    To see the list of available `invoke` commands, use the `-l` option
    ```
    ➜ invoke -l
    Available tasks:

    build             Build the Nautobot docker image with the plugin installed.
    ...
    ```
Each command can be executed with `invoke <command>`.
Environment variables `INVOKE_NAUTOBOT_CONSUMABLES_PYTHON_VER` and `INVOKE_NAUTOBOT_CONSUMABLES_NAUTOBOT_VER` may be specified to override the default versions.
Each command also has its own help `invoke <command> --help`

### Environment Management

- **Local**:
```no-highlight
destroy          Destroy the suppporting containers and volumes.
restart          Restart suppporting containers.
start            Start suppporting containers.
stop             Stop suppporting containers.
```

- **Docker**:
```no-highlight
build               Build the Nautobot docker image with the plugin installed.
debug               Start Nautobot and/or its dependencies in debug mode.
destroy             Destroy containers and volumes for Nautobot and/or its dependencies.
exec                Run a command inside a container (defaults to bash shell inside nautobot container).
export              Export docker compose configuration to `compose.yaml` file.
logs                View the logs of a docker-compose service.
restart             Restart the virtual cluster.
start               Start Nautobot and/or its dependencies in detached mode.
stop                Stop Nautobot and/or its dependencies.
```

### Utility

```no-highlight
cli                 Launch a bash shell inside the running Nautobot container.
create-env          Add a base set of data to Nautobot to make development easier.
createsuperuser     Create a new Nautobot superuser account (default: "admin"), will prompt for password.
dbshell             Start database client inside the running `db` container.
generate-packages   Generate all python packages inside a docker container and copy them to ./dist
help                Show the help messages for all configured tasks.
import-db           Stop the Nautobot containers and import a database dump file.
lock                Generate the poetry.lock file in the Nautobot container
makemigrations      Perform the Django `makemigrations` operation.
migrate             Perform the Django migrate operation.
mkdocs              Runs `mkdocs` to create the static documentation for the plugin.
nbshell             Launch an interactive nbshell session.
post-upgrade        Performs common Nautobot post-upgrade operations using a single entrypoint.
shell-plus          Launch and interactive shell_plus session.
showmigrations      Show the list of all applied migrations.
```

### Testing

```no-highlight
test.bandit         Run bandit to validate basic static code security analysis.
test.coverage       Report on test coverage as measured by `invoke test.unittests`.
test.everything     Run all the linters and pytest with coverage.
test.flake8         Check for PEP8 compliance and style issues.
test.mypy           Check for proper type hinting.
test.pydocstyle     Validate docstring formats.
test.pylint         Run pylint code analysis.
test.unittests      Run the plugin tests with coverage.
```

## Tips

### Creating a Superuser

The Nautobot development image will automatically provision a superuser when specifying the following variables within `creds.env` which is the default when copying `creds.example.env` to `creds.env`:

- `NAUTOBOT_CREATE_SUPERUSER=true`
- `NAUTOBOT_SUPERUSER_API_TOKEN=0123456789abcdef0123456789abcdef01234567`
- `NAUTOBOT_SUPERUSER_PASSWORD=admin`

!!! note
	The default username is **admin**, but can be overridden by specifying **NAUTOBOT_SUPERUSER_USERNAME**.

If you need to create additional superusers, run the follow commands.

```bash
➜ invoke createsuperuser
Running docker-compose command "ps --services --filter status=running"
Running docker-compose command "exec nautobot nautobot-server createsuperuser --username admin"
Error: That username is already taken.
Username: batman
Email address: batman@example.com
Password:
Password (again):
Superuser created successfully.
```

### Python Shell

To drop into a Django shell for Nautobot (in the Docker container) run:

```bash
➜ invoke nbshell
```

This is the same as running:

```bash
➜ invoke cli
➜ nautobot-server nbshell
```

### iPython Shell Plus

Django also has a more advanced shell that uses iPython and that will automatically import all the models:

```bash
➜ invoke shell-plus
```

This is the same as running:

```bash
➜ invoke cli
➜ nautobot-server shell_plus
```

### Tests

To run tests against your code, you can run all of the tests that TravisCI runs against any new PR with:

```bash
➜ invoke test.everything
```

To run an individual test, you can run any or all of the following:

```bash
➜ invoke test.pylint
➜ invoke test.flake8
➜ invoke test.pydocstyle
➜ invoke test.mypy
➜ invoke test.bandit
➜ invoke test.unittests
➜ invoke test.coverage
```

!!! tip
    To speed testing up when developing, use the `-k` flag with `test.unittests` or `test.everything` to preserve the test database.
    The data created during tests will still be cleaned out, but the database itself will be maintained, meaning that the test suite doesn't have to create it and run the full set of migrations every time.


## To Rebuild or Not to Rebuild

Most of the time, you will not need to rebuild your images. Simply running `invoke start` and `invoke stop` is enough to keep your environment going.
However there are a couple of instances when you will want to.

### Updating Environment Variables

To add environment variables to your containers, thus allowing Nautobot to use them, you will update/add them in the `development/development.env` file.
However, doing so is considered updating the underlying container shell, instead of Django (which auto restarts itself on changes).

To get new environment variables to take effect, you will need stop any running images, rebuild the images, then restart them.
This can easily be done with 3 commands:

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

Once completed, the new/updated environment variables should now be live.

### Installing Additional Python Packages

If you want your Nautobot app to leverage another available Nautobot app or another Python package, you can easily add them into your Docker environment.

```bash
➜ poetry shell
➜ poetry add <package_name>
```

Once the dependencies are resolved, stop the existing containers, rebuild the Docker image, and then start all containers again.

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

### Installing Additional Nautobot Apps

Let's say for example you want the new Nautobot app you're creating to integrate with Nautobot Consumables.
To do this, you will want to add the Nautobot Consumables app to your environment.

```bash
➜ poetry shell
➜ poetry add nautobot-fsus
```

Once you activate the virtual environment via Poetry, you then tell Poetry to install the new Nautobot app.

Before you continue, you'll need to update the file `development/nautobot_config.py` accordingly, adding `nautobot_fsus` to the `PLUGINS` and any relevant settings as necessary under `PLUGINS_CONFIG`.
Since you're modifying the underlying OS (not just Django files), you need to rebuild the image.
This is a similar process to updating environment variables, which was explained earlier.

```bash
➜ invoke stop
➜ invoke build
➜ invoke start
```

Once the containers are up and running, you should now see the new Nautobot app installed in your Nautobot instance.

!!! note
    You can even launch an `ngrok` service locally on your laptop, pointing to port 8080 (such as for SSoT development), and it will point traffic directly to your Docker images.

### Updating Python Version

To update the Python version, you can update it in your `invoke.yml` file:

```yaml
nautobot_fsus:
  project_name: "nautobot-fsus"
  project_source: "nautobot_fsus"
  nautobot_ver: "1.6.21"
  local: false
  python_ver: "3.12"
```

Or in `tasks/__init__.py`:

```python
namespace.configure(
    {
        "nautobot_fsus": {
            ...
            "python_ver": "3.12",
	    ...
        }
    }
)
```

Or set the `INVOKE_NAUTOBOT_CONSUMABLES_PYTHON_VER` variable.

### Updating Nautobot Version

To update the Nautobot version, you can update it within `pyproject.toml`:

```toml
[tool.poetry.dependencies]
# Used for local development
python = ">=3.10,<3.12"
nautobot = "^1.6.21"
```

Or set it directly in `tasks/__init__.py`:

```python
namespace.configure(
    {
        "nautobot_fsus": {
            ...
            "nautobot_ver": "1.6.25",
	    ...
        }
    }
)
```

Or set the `INVOKE_NAUTOBOT_SSOT_NAUTOBOT_VER` variable.
