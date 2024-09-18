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

"""Tests for FSU model views defined in the Nautobot FSUs app."""
from typing import Type

from nautobot.dcim.models import Device, Location, Manufacturer
from nautobot.extras.models import Status
from nautobot.utilities.testing import ViewTestCases

from nautobot_fsus import models
from nautobot_fsus.models.mixins import FSUModel, FSUTypeModel


class FSUViewTestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for testing FSU model views."""

    class FSUModelViewTestCase(
        ViewTestCases.PrimaryObjectViewTestCase,
        ViewTestCases.BulkRenameObjectsViewTestCase,
    ):
        """Common tests for FSU model views."""

        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]

        @classmethod
        def setUpTestData(cls):
            """Set up initial test data."""
            model_name = cls.model._meta.model_name

            fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test {cls.model._meta.verbose_name}",
                    part_number="0001",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Another {cls.model._meta.verbose_name}",
                    part_number="0002",
                ),
            ]

            devices = [Device.objects.first(), Device.objects.last()]
            location = Location.objects.first()
            statuses = {
                "device": Status.objects.get(name="Active"),
                "location": Status.objects.get(name="Available"),
            }

            for i in range(3):
                cls.model.objects.create(
                    fsu_type=fsu_types[0],
                    device=devices[0],
                    name=f"test_{model_name}_{i + 1}",
                    serial_number=f"a000{i + 1}",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["device"],
                    description=f"{['First', 'Second', 'Third'][i]} test {cls.model._meta.verbose_name}",
                )

            cls.form_data = {
                "fsu_type": fsu_types[1].pk,
                "device": None,
                "location": location.pk,
                "name": f"test_{model_name}_3",
                "serial_number": "a0004",
                "firmware_version": "1.1",
                "driver_name": "new_test_driver",
                "driver_version": "1.1",
                "status": statuses["location"].id,
                "fsu_target_speed": 55,
            }

            cls.bulk_edit_data = {
                "fsu_type": fsu_types[1].pk,
                "device": devices[1].pk,
                "location": None,
            }

            cls.csv_data = (
                "device,location,name,fsu_type,status",
                f"{devices[1].name},,test_{model_name}_7,{fsu_types[1].id},active",
                f"{devices[1].name},,test_{model_name}_8,{fsu_types[1].id},active",
                f",{location.name},test_{model_name}_9,{fsu_types[1].id},available",
            )


class CPUViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for CPU model views."""

    model = models.CPU
    type_model = models.CPUType


class DiskViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for Disk model views."""

    model = models.Disk
    type_model = models.DiskType


class FanViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for Fan model views."""

    model = models.Fan
    type_model = models.FanType


class GPUViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for GPU model views."""

    model = models.GPU
    type_model = models.GPUType


class GPUBaseboardViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for GPUBaseboard model views."""

    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType


class HBAViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for HBA model views."""

    model = models.HBA
    type_model = models.HBAType


class MainboardViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for Mainboard model views."""

    model = models.Mainboard
    type_model = models.MainboardType


class NICViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for NIC model views."""

    model = models.NIC
    type_model = models.NICType


class OtherFSUViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for OtherFSU model views."""

    model = models.OtherFSU
    type_model = models.OtherFSUType


class PSUViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for PSU model views."""

    model = models.PSU
    type_model = models.PSUType


class RAMModuleViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for RAMModule model views."""

    model = models.RAMModule
    type_model = models.RAMModuleType
