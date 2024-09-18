#  SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
#  NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
#  property and proprietary rights in and to this material, related
#  documentation and any modifications thereto. Any use, reproduction,
#  disclosure or distribution of this material and related documentation
#  without an express license agreement from NVIDIA CORPORATION or
#  its affiliates is strictly prohibited.
"""Task definitions for linting and testing."""
from invoke import Context, task

from tasks import helpers


# =================================================================== #
# Linters
# =================================================================== #
@task(
    iterable=["disable", "enable"],
    help={
        "disable": "Pass the value to the pylint --disable flag, can be given multiple times.",
        "enable": "Pass the value to the pylint --enable flag, can be given multiple times.",
        "path": "Set an alternate path for pylint to check, default is nautobot_fsus",
        "verbose": "Enable verbose output for the pylint command.",
    },
)
def pylint(context: Context, path: str = "nautobot_fsus", verbose: bool = False,
           enable: list[str] | None = None, disable: list[str] | None = None) -> None:
    """Run pylint code analysis."""
    command = ["pylint", "--init-hook", "\"import nautobot; nautobot.setup()\"",
               "--rcfile", "pyproject.toml"]

    if verbose is True:
        command.append("--verbose")
    if disable is not None:
        command.extend([f"--disable={value}" for value in disable])
    if enable is not None:
        command.extend([f"--enable={value}" for value in enable])

    command.append(path)

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "verbose": "Enable verbose output for the flake8 command.",
        "show-source": "Show the source that generated each error or warning."
    },
)
def flake8(context: Context, verbose: bool = False, show_source: bool = False) -> None:
    """Check for PEP8 compliance and style issues."""
    command = ["flake8"]

    if verbose is True:
        command.append("--verbose")
    if show_source is True:
        command.append("--show-source")

    command.append("nautobot_fsus")

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "verbose": "Enable verbose output for the pydocstyle command.",
        "debug": "Print debug information.",
        "explain": "Show explanations for each error.",
        "source": "Show the source for each error.",
    },
)
def pydocstyle(context: Context, verbose: bool = False, debug: bool = False, explain: bool = False,
               source: bool = False) -> None:
    """Validate docstring formats."""
    command = ["pydocstyle"]

    if verbose is True:
        command.append("--verbose")
    if debug is True:
        command.append("--debug")
    if explain is True:
        command.append("--explain")
    if source is True:
        command.append("--source")

    command.append("nautobot_fsus")

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "verbose": "Enable verbose output for the mypy command.",
        "no-pretty": "Disable visually nicer output in error messages.",
        "no-color": "Disable Colorized error messages.",
        "no-summary": "Do not show the error status summary.",
    },
)
def mypy(context: Context, verbose: bool = False, no_pretty: bool = False, no_color: bool = False,
         no_summary: bool = False) -> None:
    """Check for proper type hinting."""
    command = ["mypy"]

    if verbose is True:
        command.append("--verbose")
    if no_pretty is True:
        command.append("--no-pretty")
    else:
        command.append("--pretty")
    if no_color is True:
        command.append("--no-color-output")
    else:
        command.append("--color-output")
    if no_summary is True:
        command.append("--no-error-summary")
    else:
        command.append("--error-summary")

    command.append("nautobot_fsus")

    helpers.run_command(context, " ".join(command))


@task
def bandit(context: Context) -> None:
    """Run bandit to validate basic static code security analysis."""
    helpers.run_command(
        context,
        "bandit --recursive nautobot_fsus --configfile .bandit.yml",
    )


# =================================================================== #
# Tests and Coverage
# =================================================================== #
@task(
    help={
        "keepdb": "Save and re-use test database between test runs for faster re-testing.",
        "label": "Specify a directory or module to test instead of running all Nautobot tests. "
                 "Default is 'nautobot_fsus`.",
        "failfast": "Fail as soon as a single test fails don't run the entire test suite",
        "buffer": "Discard output from passing tests",
        "verbose": "Enable verbose test output.",
        "append": "Append coverage data to .coverage, otherwise it starts clean each time.",
        "report-file": "Filename to save the XML test report to, default is 'rspec.xml'.",
    }
)
def unittests(context: Context, keepdb: bool = False, label: str = "nautobot_fsus",
              failfast: bool = False, buffer: bool = True, verbose: bool = False,
              append: bool = False, report_file: str | None = None) -> None:
    """Run the plugin tests with coverage."""
    command = ["coverage run"]
    if append:
        command.append("--append")
    command.append("--module nautobot.core.cli test")
    command.append(label)

    if keepdb:
        command.append("--keepdb")
    if failfast:
        command.append("--failfast")
    if buffer:
        command.append("--buffer")
    if verbose:
        command.append("--verbosity 2")
    if report_file is not None:
        command.append(f"--report-file {report_file}")

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "covered": "Show all files, even those with 100% coverage "
                   "(default is to skip fully covered files)."
    }
)
def coverage(context: Context, covered: bool = False) -> None:
    """Report on test coverage as measured by `invoke test.unittests`."""
    command = ["coverage report"]
    if not covered:
        command.append("--skip-covered")

    helpers.run_command(context, " ".join(command))


@task(
    help={
        "keepdb": "Save and re-use test database between test runs for faster re-testing.",
        "verbose": "Enable verbose output for lint and test commands.",
    }
)
def everything(context: Context, keepdb: bool = False, verbose: bool = False) -> None:
    """Run all the linters and pytest with coverage."""
    print("Running pylint...")
    pylint(context, verbose=verbose)

    print("-" * 70)
    print("\nRunning flake8...")
    flake8(context, verbose=verbose)

    print(f"\n{('-' * 70)}\n")
    print("Running pydocstyle...")
    pydocstyle(context, verbose=verbose)

    print(f"\n{('-' * 70)}\n")
    print("Running mypy...")
    mypy(context, verbose=verbose)

    print(f"\n{('-' * 70)}\n")
    print("Running bandit...")
    bandit(context)

    print(f"\n{('-' * 70)}\n")
    print("Running tests...")
    unittests(context, keepdb=keepdb, verbose=verbose)

    print(f"\n{('-' * 70)}\n")
    print("Generating coverage report...")
    coverage(context)
