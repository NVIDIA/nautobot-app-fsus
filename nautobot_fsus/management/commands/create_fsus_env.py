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

"""Bootstrap dummy data for local testing."""
import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from nautobot.core.management.commands import generate_test_data
from nautobot.users.models import Token

from nautobot_fsus.tests.fixtures import create_env


class Command(BaseCommand):
    """Publish the command to bootstrap dummy data."""

    def add_arguments(self, parser):
        """Optional command-line arguments for the handler."""
        super().add_arguments(parser)
        parser.add_argument(
            "--seed",
            help="String to use as a random generator seed for reproducible results.",
        )
        parser.add_argument(
            "--cache-fixtures",
            action="store_true",
            help="Save the generated test data to a json fixture file to re-use if the fixture "
                 "file is not found, load the previously generated test data from the fixture "
                 "file if it exists (implies the --flush option).",
        )
        parser.add_argument(
            "--fixture-file",
            default="development/factory_dump.json",
            help="Fixture file to use with --cache-fixtures.",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush any existing data in the database before generating new test data."
        )
        parser.add_argument(
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Do NOT prompt the user for input or confirmation of any kind.",
        )
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='The database to generate the test data in. Defaults to the "default" database.',
        )

    def _create_superuser(self):
        """Create the default superuser account."""
        # After a database flush, the admin account needs to be recreated.
        username = os.environ.get("NAUTOBOT_SUPERUSER_NAME", "admin")
        password = os.environ.get("NAUTOBOT_SUPERUSER_PASSWORD", "admin")
        email = os.environ.get("NAUTOBOT_SUPERUSER_EMAIL", "admin@example.com")
        token = os.environ.get(
            "NAUTOBOT_SUPERUSER_TOKEN",
            "0123456789abcdef0123456789abcdef01234567"
        )

        admin_user = get_user_model().objects.filter(username=username)
        if not admin_user:
            admin_user = get_user_model().objects.create_superuser(username, email, password)
            Token.objects.create(user=admin_user, key=token)
        else:
            admin_user = admin_user[0]
            if admin_user.email != email:
                admin_user.email = email
            if not admin_user.check_password(password):
                admin_user.set_password(password)
            admin_user.save()
            admin_token = Token.objects.filter(user=admin_user)
            if admin_token:
                admin_token = admin_token[0]
                if admin_token.key != token:
                    admin_token.key = token
                    admin_token.save()

    def handle(self, *args, **options):
        """Command handler method."""
        if options["cache_fixtures"]:
            options["flush"] = True
            options["interactive"] = False

        db_name = connections[options['database']].settings_dict['NAME']
        if options["flush"]:
            if options["interactive"]:
                confirmation = input(f"""
You have requested a flush of the database before generating new data. This will
IRREVERSIBLY DESTROY all data in the "{db_name}" database, including all user accounts,
and return each table to an empty state. Are you sure you want to do this?

Type "yes" to continue, or "no" to cancel: """)
                if confirmation.lower() != "yes":
                    self.stdout.write(self.style.ERROR("Canceled."))
                    return

            self.stdout.write(
                self.style.WARNING(
                    f"Flushing all existing data from the {options['database']} database..."
                )
            )
            call_command("flush", "--no-input", "--database", options['database'])

        if options["cache_fixtures"] and os.path.exists(options["fixture_file"]):
            call_command("loaddata", options["fixture_file"])
        else:
            self.stdout.write(self.style.MIGRATE_HEADING("Populating Nautobot factory test data"))
            if not db_name.startswith("test"):
                self._create_superuser()
            seed = options.get("seed", get_random_string(16))
            try:
                generate_test_data.Command()._generate_factory_data(  # pylint: disable=W0212
                    seed,
                    options['database'],
                )
            except ValidationError:
                self.stdout.write(
                    self.style.WARNING(
                        "It appears that the base Nautobot factory data has already been "
                        "populated. If you want to regenerate it fresh, re-run the command with "
                        "the `--flush` flag."
                    )
                )
            try:
                create_env(seed=seed)
            except IntegrityError as error:
                self.stdout.write(
                    self.style.ERROR(
                        f"Unable to populate data, command is not idempotent. "
                        f"Please validate objects do not already exist.\n"
                        f"{error}"
                    )
                )

            if options["cache_fixtures"]:
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
                    output=options["fixture_file"],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Dumped fixture data to {options['fixture_file']}."
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Database {options['database']} successfully populated."
                )
            )
