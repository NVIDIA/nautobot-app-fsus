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

"""Tests for FSU Type models defined by the Nautobot FSUS app."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from nautobot.dcim.models import Manufacturer

from nautobot_fsus import models


class FSUTypeTestCase(TestCase):
    """Test case for FSU type models."""

    def test_export_fsu_type(self):  # pylint: disable=too-many-statements
        """Test exporting an FSU type model to CSV."""
        with self.subTest(fsu_type="cputype"):
            instance = models.CPUType(
                manufacturer=Manufacturer.objects.first(),
                name="Test CPU",
                part_number="0001",
                architecture="arm",
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 8)
            self.assertEqual(csv[3], "arm")

        with self.subTest(fsu_type="disktype"):
            instance = models.DiskType(
                manufacturer=Manufacturer.objects.first(),
                name="Test Disk",
                part_number="2001",
                disk_type="NVME",
                size=1024,
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 7)
            self.assertEqual(csv[3], "NVME")

        with self.subTest(fsu_type="gpubaseboardtype"):
            instance = models.GPUBaseboardType(
                manufacturer=Manufacturer.objects.first(),
                name="Test Baseboard",
                part_number="0001",
                slot_count=8,
            )
            instance.save()

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 6)
            self.assertEqual(csv[3], "8")

        with self.subTest(fsu_type="gputype"):
            instance = models.GPUType(
                manufacturer=Manufacturer.objects.first(),
                name="Test GPU",
                part_number="0001",
            )
            instance.save()

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 5)
            self.assertEqual(csv[1], instance.name)

        with self.subTest(fsu_type="hbatype"):
            instance = models.HBAType(
                manufacturer=Manufacturer.objects.first(),
                name="Test HBA",
                part_number="0001",
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 5)
            self.assertEqual(csv[1], instance.name)

        with self.subTest(fsu_type="mainboard"):
            instance = models.MainboardType(
                manufacturer=Manufacturer.objects.first(),
                name="Test Mainboard",
                part_number="0001",
                pcie_generation=7,
                cpu_socket_count=4,
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 7)
            self.assertEqual(csv[3], "7.x")
            self.assertEqual(csv[4], "4")

        with self.subTest(fsu_type="nictype"):
            instance = models.NICType(
                manufacturer=Manufacturer.objects.first(),
                name="Test NIC",
                part_number="0001",
                interface_count=4,
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 6)
            self.assertEqual(csv[3], "4")

        with self.subTest(fsu_type="psutype"):
            instance = models.PSUType(
                manufacturer=Manufacturer.objects.first(),
                name="Test PSU",
                part_number="1001",
                power_provided=1000,
                hot_swappable=True,
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 9)
            self.assertEqual(csv[3], "DC")

        with self.subTest(fsu_type="rammoduletype"):
            instance = models.RAMModuleType(
                manufacturer=Manufacturer.objects.first(),
                name="Test DIMM",
                part_number="3001",
                capacity=64,
            )
            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 10)
            self.assertEqual(csv[3], "UDIMM")
            self.assertEqual(csv[4], "DDR5")
            self.assertEqual(csv[6], "64")
            self.assertEqual(csv[7], "1")

    def test_fsutype_duplicate_part_number(self):
        """Verify unique part number constraint for FSU types."""
        instance1 = models.NICType(
            manufacturer=Manufacturer.objects.first(),
            name="Test NIC",
            part_number="0001",
        )
        instance1.validated_save()

        instance2 = models.NICType(
            manufacturer=Manufacturer.objects.first(),
            name="Test NIC 2",
            part_number="0001",
        )

        # Same manufacturer and part number should fail
        with self.assertRaises(ValidationError):
            instance2.full_clean()

        # Different manufacturer, but same part number should pass
        instance2.manufacturer = Manufacturer.objects.last()
        instance2.full_clean()


