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

"""Tests for filters defined in the Nautobot FSUs app."""
from nautobot.dcim.models import Device, Manufacturer
from nautobot.extras.models import Status

from nautobot_fsus import filters, models
from nautobot_fsus.utilities.testing import FSUFilterTestCases


class CPUTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for CPU filters."""
    model = models.CPU
    type_model = models.CPUType
    queryset = models.CPU.objects.all()
    filterset = filters.CPUFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the test case."""
        super().setUpTestData()

        mainboard_type = models.MainboardType.objects.create(
            manufacturer=Manufacturer.objects.first(),
            name="Test Mainboard Type",
            part_number="A10001",
        )

        mainboard = models.Mainboard.objects.create(
            fsu_type=mainboard_type,
            device=cls.device,
            name="Test Mainboard",
            serial_number="mb1",
            firmware_version="1.0",
            driver_name="test_driver",
            driver_version="1.0",
            description="Mainboard",
            status=Status.objects.get(slug="active"),
        )

        cls.fsus[0].parent_mainboard = mainboard
        cls.fsus[0].validated_save()

    def test_has_parent_mainboard_filter(self):
        """Test filtering on CPUs that have a parent Mainboard."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"has_parent_mainboard": True}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_cpu_0")

    def test_parent_mainboard_filter(self):
        """Test filtering on a CPU's parent mainboard."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"parent_mainboard": ["Test Mainboard"]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_cpu_0")


class DiskTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for Disk filters."""
    model = models.Disk
    type_model = models.DiskType
    queryset = models.Disk.objects.all()
    filterset = filters.DiskFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the test case."""
        super().setUpTestData()

        hba_type = models.HBAType.objects.create(
            manufacturer=Manufacturer.objects.first(),
            name="Test HBA Type",
            part_number="A10001",
        )

        hba = models.HBA.objects.create(
            fsu_type=hba_type,
            device=cls.device,
            name="Test HBA",
            serial_number="hba1",
            firmware_version="1.0",
            driver_name="test_driver",
            driver_version="1.0",
            description="HBA",
            status=Status.objects.get(slug="active"),
        )

        cls.fsus[0].parent_hba = hba
        cls.fsus[0].validated_save()

    def test_has_parent_hba_filter(self):
        """Test filtering on Disks that have a parent HBA."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"has_parent_hba": True}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_disk_0")

    def test_parent_hba_filter(self):
        """Test filtering on a Disk's parent HBA."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"parent_hba": ["Test HBA"]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_disk_0")


class FanTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for Fan Filters."""
    model = models.Fan
    type_model = models.FanType
    queryset = models.Fan.objects.all()
    filterset = filters.FanFilterSet


class GPUBaseboardTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for Baseboard filters."""
    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType
    queryset = models.GPUBaseboard.objects.all()
    filterset = filters.GPUBaseboardFilterSet


class GPUTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for GPU filters."""
    model = models.GPU
    type_model = models.GPUType
    queryset = models.GPU.objects.all()
    filterset = filters.GPUFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the test case."""
        super().setUpTestData()

        gpubaseboard_type = models.GPUBaseboardType.objects.create(
            manufacturer=Manufacturer.objects.first(),
            name="Test Baseboard Type",
            slot_count=8,
        )

        gpubaseboard = models.GPUBaseboard.objects.create(
            fsu_type=gpubaseboard_type,
            device=Device.objects.first(),
            name="Test Parent",
            serial_number="bb8",
            firmware_version="1.0",
            driver_name="test_driver",
            driver_version="1.0",
            description="GPU Baseboard",
            status=Status.objects.get(slug="active"),
        )

        gpubaseboard.gpus.set([cls.fsus[0]])
        gpubaseboard.validated_save()

    def test_has_parent_baseboard_filter(self):
        """Test filtering on GPUs that have a parent Baseboard."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"has_parent_gpubaseboard": True}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_gpu_0")

    def test_parent_baseboard_filter(self):
        """Test filtering on a GPU's parent Baseboard."""
        self.assertGreater(self.queryset.count(), 1)
        params = {"parent_gpubaseboard": ["Test Parent"]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, "test_gpu_0")


class HBATestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for HBA filters."""
    model = models.HBA
    type_model = models.HBAType
    queryset = models.HBA.objects.all()
    filterset = filters.HBAFilterSet


class MainboardTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for Mainboard filters."""
    model = models.Mainboard
    type_model = models.MainboardType
    queryset = models.Mainboard.objects.all()
    filterset = filters.MainboardFilterSet


class NICTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for NIC filters."""
    model = models.NIC
    type_model = models.NICType
    queryset = models.NIC.objects.all()
    filterset = filters.NICFilterSet


class OtherFSUTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for OtherFSU filters."""
    model = models.OtherFSU
    type_model = models.OtherFSUType
    queryset = models.OtherFSU.objects.all()
    filterset = filters.OtherFSUFilterSet


class PSUTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for PSU filters."""
    model = models.PSU
    type_model = models.PSUType
    queryset = models.PSU.objects.all()
    filterset = filters.PSUFilterSet


class RAMModuleTestCase(FSUFilterTestCases.FSUModelFilterTestCase):
    """Tests for RAM Module filters."""
    model = models.RAMModule
    type_model = models.RAMModuleType
    queryset = models.RAMModule.objects.all()
    filterset = filters.RAMModuleFilterSet


class CPUTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for CPU template filters."""
    model = models.CPUTemplate
    type_model = models.CPUType
    queryset = models.CPUTemplate.objects.all()
    filterset = filters.CPUTemplateFilterSet


class DiskTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for Disk template filters."""
    model = models.DiskTemplate
    type_model = models.DiskType
    queryset = models.DiskTemplate.objects.all()
    filterset = filters.DiskTemplateFilterSet


class FanTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for Fan template filters."""
    model = models.FanTemplate
    type_model = models.FanType
    queryset = models.FanTemplate.objects.all()
    filterset = filters.FanTemplateFilterSet


class GPUBaseboardTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for Baseboard template filters."""
    model = models.GPUBaseboardTemplate
    type_model = models.GPUBaseboardType
    queryset = models.GPUBaseboardTemplate.objects.all()
    filterset = filters.GPUBaseboardTemplateFilterSet


class GPUTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for GPU template filters."""
    model = models.GPUTemplate
    type_model = models.GPUType
    queryset = models.GPUTemplate.objects.all()
    filterset = filters.GPUTemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load/create initial data for the tests."""
        super().setUpTestData()

        cls.templates[0].pci_slot_id = "0:000:1.0"
        cls.templates[1].pci_slot_id = "0:000:2.0"
        cls.templates[2].pci_slot_id = "0:000:1.1"

        for template in cls.templates:
            template.validated_save()
            template.refresh_from_db()


class HBATemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for HBA template filters."""
    model = models.HBATemplate
    type_model = models.HBAType
    queryset = models.HBATemplate.objects.all()
    filterset = filters.HBATemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load/create initial data for the tests."""
        super().setUpTestData()

        cls.templates[0].pci_slot_id = "0:000:1.0"
        cls.templates[1].pci_slot_id = "0:000:2.0"
        cls.templates[2].pci_slot_id = "0:000:1.1"

        for template in cls.templates:
            template.validated_save()
            template.refresh_from_db()


class MainboardTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for Mainboard template filters."""
    model = models.MainboardTemplate
    type_model = models.MainboardType
    queryset = models.MainboardTemplate.objects.all()
    filterset = filters.MainboardTemplateFilterSet


class NICTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for NIC template filters."""
    model = models.NICTemplate
    type_model = models.NICType
    queryset = models.NICTemplate.objects.all()
    filterset = filters.NICTemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load/create initial data for the tests."""
        super().setUpTestData()

        cls.templates[0].pci_slot_id = "0:000:1.0"
        cls.templates[1].pci_slot_id = "0:000:2.0"
        cls.templates[2].pci_slot_id = "0:000:1.1"

        for template in cls.templates:
            template.validated_save()
            template.refresh_from_db()


class OtherFSUTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for OtherFSU template filters."""
    model = models.OtherFSUTemplate
    type_model = models.OtherFSUType
    queryset = models.OtherFSUTemplate.objects.all()
    filterset = filters.OtherFSUTemplateFilterSet


class PSUTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for PSU template filters."""
    model = models.PSUTemplate
    type_model = models.PSUType
    queryset = models.PSUTemplate.objects.all()
    filterset = filters.PSUTemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load/create initial data for the tests."""
        super().setUpTestData()

        cls.templates[0].redundant = True
        cls.templates[0].validated_save()
        cls.templates[0].refresh_from_db()

    def test_redundant(self):
        """Test filtering on the redundant setting."""
        self.assertEqual(self.filterset({"redundant": True}, self.queryset).qs.count(), 1)


class RAMModuleTemplateTestCase(FSUFilterTestCases.FSUTemplateFilterTestCase):
    """Tests for RAM Module template filters."""
    model = models.RAMModuleTemplate
    type_model = models.RAMModuleType
    queryset = models.RAMModuleTemplate.objects.all()
    filterset = filters.RAMModuleTemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        """Load/create initial data for the tests."""
        super().setUpTestData()

        cls.templates[0].slot_id = "A1"
        cls.templates[1].slot_id = "B2"
        cls.templates[1].slot_id = "C3"

        for template in cls.templates:
            template.validated_save()
            template.refresh_from_db()


class CPUTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for CPU type filters."""
    model = models.CPU
    type_model = models.CPUType
    queryset = models.CPUType.objects.all()
    filterset = filters.CPUTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up CPUType-specific test data."""
        super().setUpTestData()

        cls.types[0].cpu_speed = 1.5
        cls.types[0].cores = 8
        cls.types[0].pcie_generation = 5
        cls.types[0].validated_save()
        cls.types[0].refresh_from_db()

        cls.types[1].architecture = "arm"
        cls.types[1].cpu_speed = 3.0
        cls.types[1].cores = 32
        cls.types[1].pcie_generation = 6
        cls.types[1].validated_save()
        cls.types[1].refresh_from_db()

    def test_cpu_arch(self):
        """Test filtering on CPU architecture."""
        params = {"architecture": ["arm"]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, self.types[1].name)

    def test_cpu_speed(self):
        """Test filtering on CPU speed."""
        with self.subTest(filter="exact"):
            params = {"cpu_speed": [3.0]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="lt"):
            params = {"cpu_speed__lt": [3.0]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="lte"):
            params = {"cpu_speed__lte": [3.0]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="gt"):
            params = {"cpu_speed__gt": [1.5]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="gte"):
            params = {"cpu_speed__gte": [1.5]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

    def test_cores(self):
        """Test filtering on CPU cores."""
        with self.subTest(filter="exact"):
            params = {"cores": [8]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="lt"):
            params = {"cores__lt": [32]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="lte"):
            params = {"cores__lte": [32]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="gt"):
            params = {"cores__gt": [8]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="gte"):
            params = {"cores__gte": [8]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

    def test_pcie_generation(self):
        """Test filtering on PCIe generation."""
        params = {"pcie_generation": [6]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, self.types[1].name)


class DiskTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for DiskType filters."""
    model = models.Disk
    type_model = models.DiskType
    queryset = models.DiskType.objects.all()
    filterset = filters.DiskTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up DisktType-specific test data."""
        super().setUpTestData()

        cls.types[0].size = 256
        cls.types[1].size = 512

        for disktype in cls.types:
            disktype.validated_save()
            disktype.refresh_from_db()

    def test_disk_size(self):
        """Test filtering on disk size."""
        with self.subTest(filter="exact"):
            params = {"size": [256]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="lt"):
            params = {"size__lt": [512]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.last().name, self.types[0].name)

        with self.subTest(filter="lte"):
            params = {"size__lte": [512]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="gt"):
            params = {"size__gt": [256]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.last().name, self.types[1].name)

        with self.subTest(filter="gte"):
            params = {"size__gte": [256]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)


class FanTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for FanType filters."""
    model = models.Fan
    type_model = models.FanType
    queryset = models.FanType.objects.all()
    filterset = filters.FanTypeFilterSet


class GPUBaseboardTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for BaseboardType filters."""
    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType
    queryset = models.GPUBaseboardType.objects.all()
    filterset = filters.GPUBaseboardTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up BaseboardType-specific test data."""
        super().setUpTestData()

        cls.types[1].slot_count = 8
        cls.types[1].validated_save()
        cls.types[1].refresh_from_db()

    def test_gpu_count(self):
        """Test filtering on gpu count."""
        params = {"slot_count__gt": [6]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, self.types[1].name)


class GPUTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for GPUType filters."""
    model = models.GPU
    type_model = models.GPUType
    queryset = models.GPUType.objects.all()
    filterset = filters.GPUTypeFilterSet


class HBATypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for HBAType filters."""
    model = models.HBA
    type_model = models.HBAType
    queryset = models.HBAType.objects.all()
    filterset = filters.HBATypeFilterSet


class MainboardTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for MainboardType filters."""
    model = models.Mainboard
    type_model = models.MainboardType
    queryset = models.MainboardType.objects.all()
    filterset = filters.MainboardTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up MainboardType-specific test data."""
        super().setUpTestData()

        cls.types[0].cpu_socket_count = 4
        cls.types[0].validated_save()
        cls.types[0].refresh_from_db()
        cls.types[1].cpu_socket_count = 2
        cls.types[1].validated_save()
        cls.types[1].refresh_from_db()

    def test_cpu_socket_count(self):
        """Test filtering on CPU socket count."""
        with self.subTest(filter="exact"):
            params = {"cpu_socket_count": [2]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="lt"):
            params = {"cpu_socket_count__lt": [4]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.last().name, self.types[1].name)

        with self.subTest(filter="lte"):
            params = {"cpu_socket_count__lte": [4]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="gt"):
            params = {"cpu_socket_count__gt": [2]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.last().name, self.types[0].name)

        with self.subTest(filter="gte"):
            params = {"cpu_socket_count__gte": [2]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)


class NICTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for NICType filters."""
    model = models.NIC
    type_model = models.NICType
    queryset = models.NICType.objects.all()
    filterset = filters.NICTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up NICType-specific test data."""
        super().setUpTestData()

        cls.types[1].interface_count = 4
        cls.types[1].validated_save()
        cls.types[1].refresh_from_db()

    def test_interface_count(self):
        """Test filtering on interface count."""
        params = {"interface_count__gt": [2]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, self.types[1].name)


class OtherFSUTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for OtherFSUType filters."""
    model = models.OtherFSU
    type_model = models.OtherFSUType
    queryset = models.OtherFSUType.objects.all()
    filterset = filters.OtherFSUTypeFilterSet


class PSUTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for PSUType filters."""
    model = models.PSU
    type_model = models.PSUType
    queryset = models.PSUType.objects.all()
    filterset = filters.PSUTypeFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up PSUType-specific test data."""
        super().setUpTestData()

        cls.types[1].feed_type = "ac"
        cls.types[0].power_provided = 550
        cls.types[1].power_provided = 1000
        cls.types[0].required_voltage = "-40V - -72V"
        cls.types[1].required_voltage = "100-240V"
        cls.types[0].hot_swappable = True

        for psu in cls.types:
            psu.validated_save()
            psu.refresh_from_db()

    def test_feed_type(self):
        """Test filtering on feed type."""
        params = {"feed_type": ["ac"]}
        filter_result = self.filterset(params, self.queryset).qs
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result.first().name, self.types[1].name)

    def test_power_provided(self):
        """Test filtering on power provided."""
        with self.subTest(filter="exact"):
            params = {"power_provided": [1000]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="lt"):
            params = {"power_provided__lt": [1000]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="lte"):
            params = {"power_provided__lte": [1000]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="gt"):
            params = {"power_provided__gt": [550]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="gte"):
            params = {"power_provided__gte": [550]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

    def test_required_voltage(self):
        """Test filtering on required voltage."""
        with self.subTest(filter="exact"):
            params = {"required_voltage": ["100-240V"]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)

        with self.subTest(filter="ic"):
            params = {"required_voltage__ic": ["72v"]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="re"):
            params = {"required_voltage__re": [".*40V.*"]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 2)

        with self.subTest(filter="isw"):
            params = {"required_voltage__isw": ["-40V"]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[0].name)

        with self.subTest(filter="iew"):
            params = {"required_voltage__iew": ["40V"]}
            filter_result = self.filterset(params, self.queryset).qs
            self.assertEqual(filter_result.count(), 1)
            self.assertEqual(filter_result.first().name, self.types[1].name)


class RAMModuleTypeTestCase(FSUFilterTestCases.FSUTypeFilterTestCase):
    """Tests for RAMModuleType filters."""
    model = models.RAMModule
    type_model = models.RAMModuleType
    queryset = models.RAMModuleType.objects.all()
    filterset = filters.RAMModuleTypeFilterSet
