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
from nautobot.dcim.models import (
    Device,
    DeviceRole,
    DeviceType,
    Location,
    LocationType,
    Manufacturer,
    Site,
)
from nautobot.extras.models import Status
from nautobot.utilities.choices import ColorChoices

from nautobot_fsus import models
from nautobot_fsus.models.mixins import FSUModel, FSUTypeModel


def create_site() -> Site:
    """Add a test Site instance."""
    site, _ = Site.objects.get_or_create(name="Site 1")
    return site


def create_location_type() -> LocationType:
    """Add a Building LocationType."""
    location_type, _ = LocationType.objects.get_or_create(name="Building")
    return location_type


def create_locations(site: Site, location_type: LocationType) -> list[Location]:
    """Add test Location instances."""
    locations: list[Location] = []
    for num in range(1, 6):
        added, _ = Location.objects.get_or_create(
            name=f"Location {num}",
            location_type=location_type,
            site=site,
        )
        locations.append(added)

    return locations


def create_manufacturers() -> list[Manufacturer]:
    """Add test Manufacturer instances."""
    manufacturers: list[Manufacturer] = []
    for num in range(1, 6):
        mfgr, _ = Manufacturer.objects.get_or_create(name=f"Manufacturer {num}")
        manufacturers.append(mfgr)

    return manufacturers


def create_devices(locations: list[Location]) -> list[tuple[Device, Device]]:
    """Add test Device instances."""
    site = Site.objects.first()
    manufacturer = Manufacturer.objects.first()

    devices: list[tuple[Device, Device]] = []
    device_type, _ = DeviceType.objects.get_or_create(
        manufacturer=manufacturer,
        model="Device Type 1",
        slug="device_type_1",
    )

    device_role, _ = DeviceRole.objects.get_or_create(
        name="Device Role 1",
        slug="device_role_1",
        color="ff0000",
    )

    for num in range(1, 6):
        dev1, _ = Device.objects.get_or_create(
            device_type=device_type,
            device_role=device_role,
            name=f"Device {num}-1",
            site=site,
            location=locations[num - 1],
        )

        dev2, _ = Device.objects.get_or_create(
            device_type=device_type,
            device_role=device_role,
            name=f"Device {num}-2",
            site=site,
            location=locations[num - 1],
        )

        devices.append((dev1, dev2))

    return devices


def create_fsu_types(manufacturers: list[Manufacturer]) -> dict[str, FSUTypeModel]:
    """Add test FSUType instances."""
    fsu_types: dict[str, FSUTypeModel] = {}

    for index, value in enumerate([
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
    ]):
        mfgr = index if index <= 4 else int(index / 2) - 2
        manufacturer = manufacturers[mfgr]
        fsu_type, fsu_model = value
        added, _ = fsu_type.objects.get_or_create(
            manufacturer=manufacturer,
            name=f"{fsu_type._meta.verbose_name} 1",
            part_number=f"{fsu_model}_000{index}"
        )
        fsu_types[fsu_model] = added

    return fsu_types


def create_fsus(
    fsu_types: dict[str, FSUTypeModel],
    devices: list[tuple[Device, Device]],
    locations: list[Location]
):
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
        fsu_type = fsu_types[fsu_model._meta.model_name]
        for num in range(1, 6):
            _ = fsu_model.objects.get_or_create(
                name=f"{fsu_model._meta.verbose_name} {num}-1",
                fsu_type=fsu_type,
                device=devices[num - 1][0],
                status=Status.objects.get(slug="active"),
            )
            _ = fsu_model.objects.get_or_create(
                name=f"{fsu_model._meta.verbose_name} {num}-2",
                fsu_type=fsu_type,
                location=locations[num - 1],
                status=Status.objects.get(slug="available"),
            )


def create_env():
    """Populate environment with basic test data."""
    print("Creating Base Data")

    print(" - Site")
    site = create_site()

    print(" - LocationType")
    location_type = create_location_type()

    print(" - Manufacturers")
    manufacturers = create_manufacturers()

    print(" - Locations")
    locations = create_locations(site, location_type)

    print(" - Devices")
    devices = create_devices(locations)

    print(" - FSUTypes")
    fsu_types = create_fsu_types(manufacturers)

    print(" - FSUs")
    create_fsus(fsu_types, devices, locations)
