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

"""Create test environment object fixtures."""
from django.utils.crypto import get_random_string
import factory.random
from nautobot.dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer
from nautobot.extras.models import Status

from nautobot_fsus import models
from nautobot_fsus.models.mixins import FSUTypeModel
from nautobot_fsus.signals import post_migrate_create_defaults


def create_env(seed: str | None = None):
    """Populate environment with basic test data."""
    if seed is None:
        seed = get_random_string(16)
    factory.random.reseed_random(seed)

    print("Creating Devices...")
    for num in range(1, 6):
        device_type = factory.random.randgen.choice(DeviceType.objects.all())
        device_role = factory.random.randgen.choice(DeviceRole.objects.all())
        location = factory.random.randgen.choice(Location.objects.filter(site__isnull=False))

        _ = Device.objects.get_or_create(
            device_type=device_type,
            device_role=device_role,
            name=f"Device {num}-1",
            site=location.site,
            location=location,
        )
        _ = Device.objects.get_or_create(
            device_type=device_type,
            device_role=device_role,
            name=f"Device {num}-2",
            site=location.site,
            location=location,
        )

    print("Updating statuses...")
    post_migrate_create_defaults()

    print("Creating FSUTypes...")
    fsu_types: dict[str, list[FSUTypeModel]] = {}

    for value in [
        (models.CPUType, "cpu"),
        (models.DiskType, "disk"),
        (models.FanType, "fan"),
        (models.GPUBaseboardType, "gpubaseboard"),
        (models.GPUType, "gpu"),
        (models.HBAType, "hba"),
        (models.MainboardType, "mainboard"),
        (models.NICType, "nic"),
        (models.OtherFSUType, "otherfsu"),
        (models.PSUType, "psu"),
        (models.RAMModuleType, "rammodule"),
    ]:
        fsu_type, type_model = value
        fsu_types[type_model] = []
        mfgr_used: list[Manufacturer] = []
        for num in range(1, 4):
            mfgr = factory.random.randgen.choice(Manufacturer.objects.exclude(id__in=mfgr_used))
            added, _ = fsu_type.objects.get_or_create(
                manufacturer=mfgr,
                name=f"{fsu_type._meta.verbose_name} {num}",
                part_number=f"{type_model}_000{num}"
            )
            mfgr_used.append(mfgr.pk)
            fsu_types[type_model].append(added)

    print("Creating FSUs...")
    for fsu_model in [
        models.CPU,
        models.Disk,
        models.Fan,
        models.GPU,
        models.GPUBaseboard,
        models.HBA,
        models.Mainboard,
        models.NIC,
        models.OtherFSU,
        models.PSU,
        models.RAMModule,
    ]:
        for num in range(1, 6):
            _ = fsu_model.objects.get_or_create(
                name=f"{fsu_model._meta.verbose_name} {num}-1",
                fsu_type=fsu_types[getattr(fsu_model._meta, "model_name", "")][0],
                device=factory.random.randgen.choice(Device.objects.all()),
                status=Status.objects.get(name="Active"),
            )
            _ = fsu_model.objects.get_or_create(
                name=f"{fsu_model._meta.verbose_name} {num}-2",
                fsu_type=fsu_types[getattr(fsu_model._meta, "model_name", "")][1],
                location=factory.random.randgen.choice(Location.objects.all()),
                status=Status.objects.get(name="Available"),
            )
