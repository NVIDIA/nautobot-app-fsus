# Contributing to Nautobot FSUs

Contributions are welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of features and design.

## Dev Env

The project is packaged with a light [development environment](dev_env.md) based on `docker-compose` to help with the local development of the project and to run tests.

The project leverages the following:

- Python linting and formatting are checked with `pylint`, `flake8`, and `pydocstyle`.
- Type hints are checked with `mypy`.
- Source code security is analyzed with `bandit`.
- Django unit tests to ensure the app is working properly.

Documentation is built using [mkdocs](https://www.mkdocs.org/).
The [Docker based development environment](dev_env.md#docker-development-environment) automatically starts a container hosting a live version of the documentation website on [http://localhost:8001](http://localhost:8001) that auto-refreshes when you make any changes to your local files.

## Branching Policy

The branching policy contains the following tenets:

- The `dev` branch is the primary branch to develop off of.
- PRs intended to add new features should be sourced from the `dev` branch.
- PRs intended to fix issues in the Nautobot LTM compatible release should be sourced from the latest `ltm-<major.minor>` branch instead of `dev`.

Nautobot FSUs app observes semantic versioning.
This may result in a quick turn around in minor versions to keep pace with an ever-growing feature set.

## Release Policy

Nautobot FSUs currently has no intended release schedule, and will release new features in minor versions.

When a new release, from `dev` to `main`, is created the following should happen.

- A release branch named `Release/v<major>.<minor>.<patch> is created from `dev` to freeze the release HEAD and allow further work to continue on the `dev` branch without affecting the release point.
- A PR is created from the release branch with:
    - Update the release notes in `docs/admin/release_notes/version_<major>.<minor>.md` file to reflect the changes.
    - Change the version from `<major>.<minor>.<patch>-beta` to `<major>.<minor>.<patch>` in `pyproject.toml`.
    - Set the PR to the `main` branch.
- Ensure the tests for the PR pass.
- Merge the PR.
- Create a new tag:
    - The tag should be in the form of `v<major>.<minor>.<patch>`.
    - The title should be in the form of `v<major>.<minor>.<patch>`.
    - The description should be the changes that were added to the `version_<major>.<minor>.md` document.
- If merged into `main`, then push from `main` to `dev`, in order to retain the merge commit created when the PR was merged
- A post release PR is created with:
    - Change the version from `<major>.<minor>.<patch>` to `<major>.<minor>.<patch + 1>-beta` in both `pyproject.toml`.
    - Set the PR to the proper branch, `dev`.
    - Once tests pass, merge.
