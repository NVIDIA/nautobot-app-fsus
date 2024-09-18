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

"""Tests for API endpoints defined in the Nautobot FSUs app."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from nautobot.dcim.models import Device, Interface, PowerPort
from nautobot.extras.models import Status
from rest_framework import status

from nautobot_fsus import models
from nautobot_fsus.utilities.testing import FSUAPITestCases

User = get_user_model()


class CPUAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the CPU model."""

    model = models.CPU
    type_model = models.CPUType


class CPUTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the CPUTemplate model."""

    model = models.CPUTemplate
    type_model = models.CPUType
    target_model_name = "CPU"


class CPUTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the CPUType model."""

    model = models.CPUType
    choices_fields = ["architecture", "pcie_generation"]

    @classmethod
    def setUpTestData(cls):
        """Set up the data for the tests."""
        super().setUpTestData()

        for index, fsu in enumerate(cls.fsu_types):
            fsu.architecture = "arm"
            fsu.cpu_speed = float(f"1.{index}")
            fsu.cores = (index * 8) + 8
            fsu.pcie_generation = 5
            fsu.validated_save()
            fsu.refresh_from_db()

        for index, item in enumerate(cls.create_data):
            item["architecture"] = "x86"
            item["cpu_speed"] = float(f"3.{index}")
            item["cores"] = (index * 4) + 4
            item["pcie_generation"] = 6


class DiskAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the Disk model."""

    model = models.Disk
    type_model = models.DiskType

    @classmethod
    def setUpTestData(cls):
        """Create objects and data for the test."""
        super().setUpTestData()
        cls.fsu_types[0].size = 512
        cls.fsu_types[1].size = 1024
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()


class DiskTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the DiskTemplate model."""

    model = models.DiskTemplate
    type_model = models.DiskType
    target_model_name = "Disk"


class DiskTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the DiskType model."""

    model = models.DiskType
    choices_fields = ["disk_type"]

    @classmethod
    def setUpTestData(cls):
        """Set up the data for the tests."""
        super().setUpTestData()

        for i in cls.fsu_types:
            i.size = 512
            i.validated_save()
            i.refresh_from_db()

        for i in cls.create_data:
            i["size"] = 1024


class FanAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the Fan model."""

    model = models.Fan
    type_model = models.FanType


class FanTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the FanTemplate model."""

    model = models.FanTemplate
    type_model = models.FanType
    target_model_name = "Fan"


class FanTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the FanType model."""

    model = models.FanType


class GPUAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the GPU model."""

    model = models.GPU
    type_model = models.GPUType


class GPUTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the GPUTemplate model."""

    model = models.GPUTemplate
    type_model = models.GPUType
    target_model_name = "GPU"


class GPUTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the GPUType model."""

    model = models.GPUType


class GPUBaseboardAPITestCase(FSUAPITestCases.ParentFSUAPIViewTestCase):
    """Test the API views for the GPUBaseboard model."""

    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType
    child_model = models.GPU
    child_type = models.GPUType
    child_field = "gpus"

    @classmethod
    def setUpTestData(cls):
        """Create objects and data for the test."""
        super().setUpTestData()
        cls.fsu_types[0].slot_count = 2
        cls.fsu_types[1].slot_count = 8
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()

        cls.extra_children = [
            cls.child_model.objects.create(
                fsu_type=cls.child_fsu_type,
                device=Device.objects.last(),
                name=f"test_{cls.child_model._meta.model_name}_2",
                serial_number="a0003",
                firmware_version="1.0",
                driver_name="test_driver",
                driver_version="1.0",
                status=Status.objects.get(slug="active"),
                description=f"Third test {cls.child_model._meta.verbose_name}",
            ),
            cls.child_model.objects.create(
                fsu_type=cls.child_fsu_type,
                device=Device.objects.last(),
                name=f"test_{cls.child_model._meta.model_name}_3",
                serial_number="a0004",
                firmware_version="1.0",
                driver_name="test_driver",
                driver_version="1.0",
                status=Status.objects.get(slug="active"),
                description=f"Fourth test {cls.child_model._meta.verbose_name}",
            ),
        ]

    def test_add_baseboard_with_too_many_children(self):
        """Test adding a GPUBaseboard with more GPUs than available slots."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["gpus"] = [str(x.pk) for x in self.children]
        data["gpus"].append(self.extra_children[0].pk)

        self.assertEqual(len(data["gpus"]), 3)
        self.assertEqual(self.fsu_types[0].slot_count, 2)

        self.add_permissions("nautobot_fsus.add_gpubaseboard")
        url = reverse("plugins-api:nautobot_fsus-api:gpubaseboard-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("gpus", response.data)
        error_message = response.data["gpus"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of GPUs being added to Baseboard (3) is greater than the "
            "number of available slots (2)",
            str(response.data["gpus"]),
        )

    def test_update_baseboard_with_too_many_children(self):
        """Test updating a GPUBaseboard with more GPUs than available slots."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["gpus"] = [str(x.pk) for x in self.children]

        self.add_permissions("nautobot_fsus.add_gpubaseboard")
        url = reverse("plugins-api:nautobot_fsus-api:gpubaseboard-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        baseboard_id = response.data["id"]
        self.assertEqual(models.GPUBaseboard.objects.get(id=baseboard_id).gpus.count(), 2)

        self.add_permissions("nautobot_fsus.change_gpubaseboard")
        data = [{
            "id": baseboard_id,
            "gpus": [str(self.children[1].pk)],
        }]
        data[0]["gpus"].extend([str(x.pk) for x in self.extra_children])
        self.assertEqual(len(data[0]["gpus"]), 3)
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("gpus", response.data)
        error_message = response.data["gpus"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of GPUs being added to Baseboard (3) is greater than the "
            "number of available slots (2)",
            str(error_message),
        )


class GPUBaseboardTemplateTestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the GPUBaseboard template."""

    model = models.GPUBaseboardTemplate
    type_model = models.GPUBaseboardType
    target_model_name = "GPUBaseboard"


class GPUBaseboardTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the GPUBaseboard type."""

    model = models.GPUBaseboardType


class HBAAPITestCase(FSUAPITestCases.ParentFSUAPIViewTestCase):
    """Test the API views for the HBA model."""

    model = models.HBA
    type_model = models.HBAType
    child_model = models.Disk
    child_type = models.DiskType
    child_field = "disks"


class HBATemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the HBATemplate model."""

    model = models.HBATemplate
    type_model = models.HBAType
    target_model_name = "HBA"


class HBATypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the HBAType model."""

    model = models.HBAType


class MainboardAPITestCase(FSUAPITestCases.ParentFSUAPIViewTestCase):
    """Test the API views for the Mainboard model."""

    model = models.Mainboard
    type_model = models.MainboardType
    child_model = models.CPU
    child_type = models.CPUType
    child_field = "cpus"

    @classmethod
    def setUpTestData(cls):
        """Create objects and data for the tests."""
        super().setUpTestData()
        cls.fsu_types[0].cpu_socket_count = 2
        cls.fsu_types[1].cpu_socket_count = 4
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()

        cls.extra_children = [
            cls.child_model.objects.create(
                fsu_type=cls.child_fsu_type,
                device=Device.objects.last(),
                name=f"test_{cls.child_model._meta.model_name}_2",
                serial_number="a0003",
                firmware_version="1.0",
                driver_name="test_driver",
                driver_version="1.0",
                status=Status.objects.get(slug="active"),
                description=f"Third test {cls.child_model._meta.verbose_name}",
            ),
            cls.child_model.objects.create(
                fsu_type=cls.child_fsu_type,
                device=Device.objects.last(),
                name=f"test_{cls.child_model._meta.model_name}_3",
                serial_number="a0004",
                firmware_version="1.0",
                driver_name="test_driver",
                driver_version="1.0",
                status=Status.objects.get(slug="active"),
                description=f"Fourth test {cls.child_model._meta.verbose_name}",
            ),
        ]

    def test_add_mainboard_with_too_many_children(self):
        """Test adding a Mainboard with more CPUs than available sockets."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["cpus"] = [str(x.pk) for x in self.children]
        data["cpus"].append(self.extra_children[0].pk)

        self.assertEqual(len(data["cpus"]), 3)
        self.assertEqual(self.fsu_types[0].cpu_socket_count, 2)

        self.add_permissions("nautobot_fsus.add_mainboard")
        url = reverse("plugins-api:nautobot_fsus-api:mainboard-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("cpus", response.data)
        error_message = response.data["cpus"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of CPUs being added to Mainboard (3) is greater than the "
            "number of available sockets (2)",
            str(response.data["cpus"]),
        )

    def test_update_mainboard_with_too_many_children(self):
        """Test updating a Mainboard with more CPUs than available sockets."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["cpus"] = [str(x.pk) for x in self.children]

        self.add_permissions("nautobot_fsus.add_mainboard")
        url = reverse("plugins-api:nautobot_fsus-api:mainboard-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        mainboard_id = response.data["id"]
        self.assertEqual(models.Mainboard.objects.get(id=mainboard_id).cpus.count(), 2)

        self.add_permissions("nautobot_fsus.change_mainboard")
        data = [{
            "id": mainboard_id,
            "cpus": [str(self.children[1].pk)],
        }]
        data[0]["cpus"].extend([str(x.pk) for x in self.extra_children])
        self.assertEqual(len(data[0]["cpus"]), 3)
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("cpus", response.data)
        error_message = response.data["cpus"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of CPUs being added to Mainboard (3) is greater than the "
            "number of available sockets (2)",
            str(error_message),
        )


class MainboardTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the MainboardTemplate model."""

    model = models.MainboardTemplate
    type_model = models.MainboardType
    target_model_name = "Mainboard"


class MainboardTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the MainboardType model."""

    model = models.MainboardType


class NICAPITestCase(FSUAPITestCases.ParentNonFSUChildAPIViewTestCase):
    """Test the API views for the NIC model."""

    model = models.NIC
    type_model = models.NICType
    child_model = Interface
    child_field = "interfaces"

    @classmethod
    def setUpTestData(cls):
        """Fix the test data for the NIC model."""
        super().setUpTestData()
        cls.fsu_types[0].interface_count = 2
        cls.fsu_types[1].interface_count = 4
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()

        statuses = {
            "device": Status.objects.get(name="Active"),
            "location": Status.objects.get(name="Available"),
            "interface": Status.objects.get_for_model(Interface).first()
        }

        cls.children = [
            Interface.objects.create(
                device=Device.objects.first(),
                name="eth0",
                type="1000base-x-gbic",
                status=statuses["interface"],
            ),
            Interface.objects.create(
                device=Device.objects.last(),
                name="eth1",
                type="1000base-x-gbic",
                status=statuses["interface"],
            ),
        ]

        cls.extra_children = [
            Interface.objects.create(
                device=Device.objects.last(),
                name="eth2",
                type="1000base-x-gbic",
                status=statuses["interface"],
            ),
            Interface.objects.create(
                device=Device.objects.last(),
                name="eth3",
                type="1000base-x-gbic",
                status=statuses["interface"],
            ),
        ]

    def test_add_nic_with_too_many_children(self):
        """Test adding a NIC with more Interfaces than available connections."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["interfaces"] = [str(x.pk) for x in self.children]
        data["interfaces"].append(self.extra_children[0].pk)

        self.assertEqual(len(data["interfaces"]), 3)
        self.assertEqual(self.fsu_types[0].interface_count, 2)

        self.add_permissions("nautobot_fsus.add_nic")
        url = reverse("plugins-api:nautobot_fsus-api:nic-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("interfaces", response.data)
        error_message = response.data["interfaces"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of Interfaces being added to NIC (3) is greater than the number of "
            "available connections (2)",
            str(error_message)
        )

    def test_update_nic_with_too_many_children(self):
        """Test updating a NIC with more Interfaces than available connections."""
        self.children[0].device = Device.objects.last()
        self.children[0].validated_save()
        data = self.create_data[0]
        data["interfaces"] = [str(x.pk) for x in self.children]

        self.add_permissions("nautobot_fsus.add_nic")
        url = reverse("plugins-api:nautobot_fsus-api:nic-list")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_201_CREATED)
        nic_id = response.data["id"]
        self.assertEqual(models.NIC.objects.get(id=nic_id).interfaces.count(), 2)

        self.add_permissions("nautobot_fsus.change_nic")
        data = [{"id": nic_id, "interfaces": [str(self.children[1].pk)]}]
        data[0]["interfaces"].extend([str(x.pk) for x in self.extra_children])
        self.assertEqual(len(data[0]["interfaces"]), 3)
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn("interfaces", response.data)
        error_message = response.data["interfaces"]
        if isinstance(error_message, list):
            error_message = error_message[0].message
        self.assertEqual(
            "Number of Interfaces being added to NIC (3) is greater than the number of "
            "available connections (2)",
            str(error_message)
        )


class NICTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the NICTemplate model."""

    model = models.NICTemplate
    type_model = models.NICType
    target_model_name = "NIC"


class NICTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the NICType model."""

    model = models.NICType


class OtherFSUAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the OtherFSU model."""

    model = models.OtherFSU
    type_model = models.OtherFSUType


class OtherFSUTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the OtherFSUTemplate model."""

    model = models.OtherFSUTemplate
    type_model = models.OtherFSUType
    target_model_name = "OtherFSU"


class OtherFSUTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the OtherFSUType model."""

    model = models.OtherFSUType


class PSUAPITestCase(FSUAPITestCases.ParentNonFSUChildAPIViewTestCase):
    """Test the API views for the PSU model."""

    model = models.PSU
    type_model = models.PSUType
    child_model = PowerPort
    child_field = "power_ports"

    @classmethod
    def setUpTestData(cls):
        """Fix the test data for the PSU model."""
        super().setUpTestData()

        cls.children = [
            PowerPort.objects.create(
                device=Device.objects.first(),
                name="PP0",
            ),
            PowerPort.objects.create(
                device=Device.objects.last(),
                name="PP1",
            ),
        ]


class PSUTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the PSUTemplate model."""

    model = models.PSUTemplate
    type_model = models.PSUType
    target_model_name = "PSU"


class PSUTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the PSUType model."""

    model = models.PSUType
    choices_fields = ["feed_type"]

    @classmethod
    def setUpTestData(cls):
        """Set up the data for the tests."""
        super().setUpTestData()

        cls.fsu_types[0].power_provided = 500
        cls.fsu_types[1].power_provided = 600
        cls.fsu_types[2].power_provided = 700
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()

        cls.create_data[0]["power_provided"] = 800
        cls.create_data[1]["power_provided"] = 900
        cls.create_data[2]["power_provided"] = 1000


class RAMModuleAPITestCase(FSUAPITestCases.FSUAPIViewTestCase):
    """Test the API views for the RAMModule model."""

    model = models.RAMModule
    type_model = models.RAMModuleType

    @classmethod
    def setUpTestData(cls):
        """Create objects and data for the test."""
        super().setUpTestData()
        cls.fsu_types[0].capacity = 32
        cls.fsu_types[1].capacity = 64
        for i in cls.fsu_types:
            i.validated_save()
            i.refresh_from_db()

        cls.fsus[0].slot_id = "A1"
        cls.fsus[1].slot_id = "A2"
        for i in cls.fsus[:2]:
            i.validated_save()
            i.refresh_from_db()

        cls.create_data[0]["slot_id"] = "B1"
        cls.create_data[1]["slot_id"] = "B2"


class RAMModuleTemplateAPITestCase(FSUAPITestCases.FSUTemplateAPIViewTestCase):
    """Test the API views for the RAMModuleTemplate model."""

    model = models.RAMModuleTemplate
    type_model = models.RAMModuleType
    target_model_name = "RAMModule"

    @classmethod
    def setUpTestData(cls):
        """Create objects and data for the test."""
        super().setUpTestData()

        for i in cls.fsu_types:
            i.capacity = 64
            i.validated_save()
            i.refresh_from_db()

        for i in range(0, 3):
            cls.templates[i].slot_id = f"A{i}"
            cls.templates[i].validated_save()
            cls.templates[i].refresh_from_db()
            cls.create_data[i]["slot_id"] = f"B{i}"


class RAMModuleTypeAPITestCase(FSUAPITestCases.FSUTypeAPIViewTestCase):
    """Test the API views for the RAMModuleType model."""

    model = models.RAMModuleType
    choices_fields = ["module_type", "technology"]

    @classmethod
    def setUpTestData(cls):
        """Set up the data for the tests."""
        super().setUpTestData()

        for i in cls.fsu_types:
            i.capacity = 32
            i.validated_save()
            i.refresh_from_db()

        for i in cls.create_data:
            i["capacity"] = 64
