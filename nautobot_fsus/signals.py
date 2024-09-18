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

"""Signal handlers for Nautobot FSUs app."""
import logging

from django.contrib.contenttypes.models import ContentType
from nautobot.extras.models import Status

from nautobot_fsus.models import (
    CPU,
    Disk,
    Fan,
    GPU,
    GPUBaseboard,
    HBA,
    Mainboard,
    NIC,
    OtherFSU,
    PSU,
    RAMModule,
)

logger = logging.getLogger("rq.worker")


def post_migrate_create_defaults(sender, apps, **kwargs):
    """Callback function for post_migrate() -- create default Statuses."""
    statuses = ["active", "available", "maintenance", "offline"]

    fsu_models = [CPU, Disk, Fan, GPU, GPUBaseboard, HBA, Mainboard, NIC, OtherFSU, PSU, RAMModule]

    print("  Adding FSU models to Statuses")
    logger.info("Adding FSU models to Statuses")
    for model in fsu_models:
        for status in statuses:
            logger.debug("Adding %s to %s", model.__name__, status)
            Status.objects.get(slug=status).content_types.add(
                ContentType.objects.get_for_model(model)
            )
