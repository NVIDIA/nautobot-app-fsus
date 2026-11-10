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

from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings
from django.urls import reverse
from nautobot.core.testing import ViewTestCases
from nautobot.dcim.models import Device, Location, Manufacturer
from nautobot.extras.models import Status
from nautobot.users.models import ObjectPermission

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

            status_available = Status.objects.get(name="Available")
            status_active = Status.objects.get(name="Active")
            cls.csv_data = (
                "device,location,name,fsu_type,status",
                f"{devices[1].pk},,test_{model_name}_A,{fsu_types[1].id},{status_active.pk}",
                f"{devices[1].pk},,test_{model_name}_B,{fsu_types[1].id},{status_active.pk}",
                f",{location.pk},test_{model_name}_C,{fsu_types[1].id},{status_available.pk}",
            )

        @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
        def test_parent_fsu_tabs_respect_object_permissions(self):
            """FSU tabs omit objects the authenticated user cannot view."""
            self.add_permissions("dcim.view_device", "dcim.view_location")

            tab_cases = (
                (Device.objects.first(), "device_fsus_tab", "Active"),
                (Location.objects.first(), "location_fsus_tab", "Available"),
            )
            for parent, url_name, status_name in tab_cases:
                with self.subTest(tab=url_name):
                    parent_field = parent._meta.model_name
                    permitted_fsu = self.model.objects.create(
                        fsu_type=self.type_model.objects.first(),
                        name=f"permitted_{parent_field}_{self.model._meta.model_name}",
                        status=Status.objects.get(name=status_name),
                        **{parent_field: parent},
                    )
                    denied_fsu = self.model.objects.create(
                        fsu_type=self.type_model.objects.first(),
                        name=f"denied_{parent_field}_{self.model._meta.model_name}",
                        status=Status.objects.get(name=status_name),
                        **{parent_field: parent},
                    )

                    object_permission = ObjectPermission.objects.create(
                        name=f"View permitted {parent_field} {self.model._meta.model_name}",
                        constraints={"pk": permitted_fsu.pk},
                        actions=["view"],
                    )
                    object_permission.users.add(self.user)
                    object_permission.object_types.add(
                        ContentType.objects.get_for_model(self.model)
                    )

                    response = self.client.get(
                        reverse(
                            f"plugins:nautobot_fsus:{url_name}",
                            kwargs={"pk": parent.pk},
                        )
                    )

                    self.assertBodyContains(response, permitted_fsu.name)
                    self.assertBodyContains(response, denied_fsu.name, count=0)


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


class LPUModuleViewTestCase(FSUViewTestCases.FSUModelViewTestCase):
    """Tests for LPUModule model views."""

    model = models.LPUModule
    type_model = models.LPUModuleType
