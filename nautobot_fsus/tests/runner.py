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
from django.core.management import call_command
from django.conf import settings
from xmlrunner.extra.djangotestrunner import XMLTestRunner


class NautobotFSUsTestRunner(XMLTestRunner):
    """
    Version of the NautobotTestRunner that doesn't flush the database by default.
    """

    def __init__(self, cache_test_fixtures=False, **kwargs):
        self.cache_test_fixtures = cache_test_fixtures
        self.fixture_file = kwargs.get("fixture_file", "development/factory_dump.json")
        self.report_file = kwargs.get("report_file")

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
            "--report-file",
            default="rspec.xml",
            help="Filename for the saved XML test report."
        )

    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        # Remove 'testserver' that Django "helpfully" adds automatically
        # to ALLOWED_HOSTS, masking issues like #3065
        settings.ALLOWED_HOSTS.remove("testserver")
        settings.TEST_OUTPUT_VERBOSE = self.verbosity
        if self.report_file is not None:
            settings.TEST_OUTPUT_FILE_NAME = self.report_file

    def setup_databases(self, **kwargs):
        result = super().setup_databases(**kwargs)
        call_command("create_fsus_env")

        if self.cache_test_fixtures:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                indent=2,
                format="json",
                exclude=[
                    "contenttypes",
                    "django_rq",
                    "auth.permission",
                    "extras.job",
                    "extras.customfield",
                ],
                output=self.fixture_file,
            )
        return result

    def teardown_databases(self, old_config, **kwargs):
        if settings.TEST_USE_FACTORIES and old_config:
            for connection in old_config:
                db_name = connection[0].alias
                print(f'Emptying test database "{db_name}"...')
                call_command(
                    "flush",
                    "--no-input",
                    "--database",
                    db_name,
                    inhibit_post_migrate=True,
                )
                print(f"Database {db_name} emptied!")

        super().teardown_databases(old_config, **kwargs)
