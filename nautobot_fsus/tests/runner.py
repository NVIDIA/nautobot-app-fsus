#  SPDX-FileCopyrightText: Copyright (c) "2024" NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Test runner wrapper for Nautobot FSUs app."""

from django.conf import settings
from django.core.management import call_command
from django.db import connections
from django.test.utils import get_unique_databases_and_mirrors
from xmlrunner.extra.djangotestrunner import XMLTestRunner


class NautobotFSUsTestRunner(XMLTestRunner):
    """
    Version of the NautobotTestRunner that doesn't flush the database by default.
    """

    def __init__(self, cache_test_fixtures=False, **kwargs):
        self.cache_test_fixtures = cache_test_fixtures
        self.fixture_file = kwargs.get("fixture_file", "development/factory_dump.json")
        self.report_file = kwargs.get("report_file")
        self.flush = kwargs.get("flush")
        self.keepdb = kwargs.get("keepdb")

        # Assert "integration" hasn't been provided w/ --tag
        incoming_tags = kwargs.get("tags") or []
        # Assert "exclude_tags" hasn't been provided w/ --exclude-tag; else default to our own.
        incoming_exclude_tags = kwargs.get("exclude_tags") or []

        # Only include our excluded tags if "integration" isn't provided w/ --tag
        if "integration" not in incoming_tags:
            incoming_exclude_tags.append("integration")
            kwargs["exclude_tags"] = incoming_exclude_tags

        super().__init__(**kwargs)

    @classmethod
    def add_arguments(cls, parser):
        """Additional arguments for the test runner."""
        super().add_arguments(parser)
        parser.add_argument(
            "--cache-test-fixtures",
            action="store_true",
            help="Save test database to a json fixture file to re-use on subsequent tests.",
        )
        parser.add_argument(
            "--fixture-file",
            default="development/factory_dump.json",
            help="Fixture file to use with --cache-test-fixtures.",
        )
        parser.add_argument(
            "--report-file", default="rspec.xml", help="Filename for the saved XML test report."
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush any existing data in the database before generating new test data.",
        )

    def setup_test_environment(self, **kwargs):
        """Global pre-test setup."""
        super().setup_test_environment(**kwargs)

        # Remove 'testserver' that Django "helpfully" adds automatically
        # to ALLOWED_HOSTS, masking issues like #3065
        settings.ALLOWED_HOSTS.remove("testserver")

        # Update the XMLTestRunner settings if needed.
        settings.TEST_OUTPUT_VERBOSE = self.verbosity
        if self.report_file is not None:
            settings.TEST_OUTPUT_FILE_NAME = self.report_file

    def setup_databases(self, **kwargs):
        """Create the test databases and add base set of factory data."""
        test_dbs, mirrored_aliases = get_unique_databases_and_mirrors(kwargs.get("aliases", None))

        old_names = []

        for db_name, aliases in test_dbs.values():
            first_alias = None
            for alias in aliases:
                connection = connections[alias]
                old_names.append((connection, db_name, first_alias is None))

                # Create the database for the first connection
                if first_alias is None:
                    first_alias = alias
                    with self.time_keeper.timed(f"  Creating '{alias}'"):
                        connection.creation.create_test_db(
                            verbosity=self.verbosity,
                            autoclobber=not self.interactive,
                            keepdb=self.keepdb,
                            serialize=connection.settings_dict["TEST"].get("SERIALIZE", True),
                        )

                    command = ["create_fsus_env", "--flush", "--no-input"]
                    if settings.TEST_FACTORY_SEED is not None:
                        command.extend(["--seed", settings.TEST_FACTORY_SEED])
                    if self.cache_test_fixtures:
                        command.append("--cache-fixtures")
                    if self.fixture_file:
                        command.extend(["--fixture-file", self.fixture_file])

                    with self.time_keeper.timed(f"  Pre-populating test database {alias}..."):
                        db_command = [*command, "--database", alias]
                        call_command(*db_command)

                    if self.parallel > 1:
                        for index in range(self.parallel):
                            with self.time_keeper.timed(f"  Cloning '{alias}'"):
                                connection.creation.clone_test_db(
                                    suffix=str(index + 1),
                                    verbosity=self.verbosity,
                                    keepdb=False,
                                )

                else:
                    connection.creation.set_as_test_mirror(connections[first_alias].settings_dict)

        for alias, mirror_alias in mirrored_aliases.items():
            connections[alias].creation.set_as_test_mirror(connections[mirror_alias].settings_dict)

        if self.debug_sql:
            for alias in connections:
                connections[alias].force_debug_cursor = True

        return old_names

    def teardown_databases(self, old_config, **kwargs):
        """Clean up the test databases."""
        for connection, old_name, destroy in old_config:
            if destroy:
                if self.parallel > 1:
                    for index in range(self.parallel):
                        connection.creation.destroy_test_db(
                            suffix=str(index + 1),
                            verbosity=self.verbosity,
                            keepdb=False,
                        )

                db_name = connection.alias
                print(f"Cleaning up test database {db_name}...")
                call_command("flush_fsus_env", "--no-input", "--database", db_name)

                connection.creation.destroy_test_db(old_name, self.verbosity, self.keepdb)
