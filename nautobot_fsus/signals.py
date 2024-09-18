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
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from nautobot.dcim.models import Device
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


def post_migrate_create_defaults(*args, **kwargs):  # pylint: disable=unused-argument
    """Callback function for post_migrate() -- create default Statuses."""
    statuses = ["active", "available", "maintenance", "offline"]

    fsu_models = [CPU, Disk, Fan, GPU, GPUBaseboard, HBA, Mainboard, NIC, OtherFSU, PSU, RAMModule]

    print("  Adding FSU models to Statuses")
    logger.info("Adding FSU models to Statuses")
    status = ""
    try:
        for model in fsu_models:
            for status in statuses:
                logger.debug("Adding %s to %s", model.__name__, status)
                Status.objects.get(slug=status).content_types.add(
                    ContentType.objects.get_for_model(model)
                )
    except Status.DoesNotExist:
        # During testing, the test DB is flushed and the post_migrate signal is sent, meaning
        # that this method is called, but the statuses are no longer there at that moment.
        print(f"  Status {status} does not exist! Has the database been flushed?")


@receiver(post_save, sender=Device, dispatch_uid="device_creation_fsu_signal")
def create_fsus_for_new_devices(
    sender: type[Device],  # pylint: disable=unused-argument
    instance: Device,
    created: bool,
    **kwargs: Any,
) -> None:
    """
    Watch for new Device creation and instantiate any associated FSUs from the DeviceType.

    Args:
        sender: The model class of the sender (filtered for Device by the receiver wrapper).
        instance: The Device instance being saved.
        created: True if a new record was created.
        **kwargs: Any other args passed by the signal.

    Method arguments are as defined in https://docs.djangoproject.com/en/4.2/ref/signals/#post-save.
    """
    if not created:
        return

    fsu_models = [
        (CPU, instance.device_type.cputemplates.all()),
        (Disk, instance.device_type.disktemplates.all()),
        (Fan, instance.device_type.fantemplates.all()),
        (GPU, instance.device_type.gputemplates.all()),
        (GPUBaseboard, instance.device_type.gpubaseboardtemplates.all()),
        (HBA, instance.device_type.hbatemplates.all()),
        (Mainboard, instance.device_type.mainboardtemplates.all()),
        (NIC, instance.device_type.nictemplates.all()),
        (OtherFSU, instance.device_type.otherfsutemplates.all()),
        (PSU, instance.device_type.psutemplates.all()),
        (RAMModule, instance.device_type.rammoduletemplates.all()),
    ]

    for model, templates in fsu_models:
        model.objects.bulk_create([fsu.instantiate(device=instance) for fsu in templates])
