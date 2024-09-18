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
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from nautobot_fsus.tests.fixtures import create_env


class Command(BaseCommand):
    """Publish the command to bootstrap dummy data."""

    def handle(self, *args, **options):
        """Command handler method."""
        self.stdout.write("Attempting to populate dummy data.")
        try:
            create_env()
            self.stdout.write(self.style.SUCCESS("Done."))
        except IntegrityError as error:
            self.stdout.write(
                self.style.ERROR(
                    f"Unable to populate data, command is not idempotent: {error}"
                )
            )
