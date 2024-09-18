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

"""Tests for FSU models defined by the Nautobot FSUS app."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from nautobot.dcim.models import Device, Location, Manufacturer
from nautobot.extras.models import Status

from nautobot_fsus import models


class FSUTestCase(TestCase):
    """Test case for FSU models."""

    def setUp(self):
        """Set up objects for the tests."""
        manufacturer = Manufacturer.objects.first()
        self.fsu_types = {
            "cpu": models.CPUType.objects.create(
                manufacturer=manufacturer,
                name="Test CPU Type",
                part_number="0002",
            ),
            "disk": models.DiskType.objects.create(
                manufacturer=manufacturer,
                name="Test Disk Type",
                part_number="0001",
            ),
            "fan": models.FanType.objects.create(
                manufacturer=manufacturer,
                name="Test Fan Type",
                part_number="0001",
            ),
            "gpu": models.GPUType.objects.create(
                manufacturer=manufacturer,
                name="Test GPU Type",
                part_number="0001",
            ),
            "gpubaseboard": models.GPUBaseboardType.objects.create(
                manufacturer=manufacturer,
                name="Test Baseboard Type",
                part_number="0001",
            ),
            "hba": models.HBAType.objects.create(
                manufacturer=manufacturer,
                name="Test HBA Type",
                part_number="0001",
            ),
            "mainboard": models.MainboardType.objects.create(
                manufacturer=manufacturer,
                name="Test Mainboard Type",
                part_number="0001",
            ),
            "nic": models.NICType.objects.create(
                manufacturer=manufacturer,
                name="Test NIC Type",
                part_number="0001",
            ),
            "otherfsu": models.OtherFSUType.objects.create(
                manufacturer=manufacturer,
                name="Test OtherFSU Type",
                part_number="0001",
            ),
            "psu": models.PSUType.objects.create(
                manufacturer=manufacturer,
                name="Test PSU Type",
                part_number="0001",
            ),
            "rammodule": models.RAMModuleType.objects.create(
                manufacturer=manufacturer,
                name="Test RAMModule Type",
                part_number="0001",
            ),
        }
        self.fsu_models = {
            "cpu": models.CPU,
            "disk": models.Disk,
            "fan": models.Fan,
            "gpu": models.GPU,
            "gpubaseboard": models.GPUBaseboard,
            "hba": models.HBA,
            "mainboard": models.Mainboard,
            "nic": models.NIC,
            "otherfsu": models.OtherFSU,
            "psu": models.PSU,
            "rammodule": models.RAMModule,
        }
        self.device = Device.objects.first()
        self.location = Location.objects.first()

    def test_fsu_creation(self):
        """Ensure an FSU can be created."""
        for fsu, model in self.fsu_models.items():
            with self.subTest(fsu=fsu):
                instance = model(
                    fsu_type=self.fsu_types[fsu],
                    name="test_fsu",
                    status=Status.objects.get(slug="active"),
                )

                self.assertIsNone(instance.parent)
                with self.assertRaises(ValidationError):
                    instance.full_clean()

                instance.device = self.device
                instance.save()

                self.assertEqual(str(instance), instance.name)
                self.assertEqual(instance.parent, instance.device)

                self.assertEqual(str(instance), instance.name)

                object_change = instance.to_objectchange("create")
                self.assertEqual(
                    object_change.changed_object_type.model_class(),
                    instance._meta.model
                )
                self.assertEqual(object_change.changed_object_id, instance.id)
                self.assertEqual(
                    object_change.related_object_type.model_class(),
                    instance.parent._meta.model,
                )
                self.assertEqual(object_change.related_object_id, instance.parent.id)

    def test_export_fsu(self):
        """Test exporting FSU model to CSV."""
        for fsu in ("gpu", "hba", "nic"):
            with self.subTest(fsu=fsu):
                instance = self.fsu_models[fsu](
                    fsu_type=self.fsu_types[fsu],
                    device=self.device,
                    name="test_fsu",
                    pci_slot_id="00000000:07:00.0",
                    status=Status.objects.get(slug="active"),
                )
                instance.save()

                columns = 14 if fsu == "gpu" else 13
                csv = instance.to_csv()
                self.assertIsInstance(csv, tuple)
                self.assertEqual(len(csv), columns)
                self.assertEqual(csv[0], str(self.device.id))
                self.assertEqual(csv[8], instance.pci_slot_id)

        with self.subTest(fsu="psu"):
            instance = self.fsu_models["psu"](
                fsu_type=self.fsu_types["psu"],
                device=self.device,
                name="test_fsu",
                redundant=True,
                status=Status.objects.get(slug="active"),
            )
            instance.save()

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 13)
            self.assertEqual(csv[2], instance.name)
            self.assertTrue(instance.redundant)

        with self.subTest(fsu="rammodule"):
            instance = self.fsu_models["rammodule"](
                fsu_type=self.fsu_types["rammodule"],
                device=self.device,
                name="test_fsu",
                slot_id="A1",
                status=Status.objects.get(slug="active"),
            )
            instance.save()

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), 13)
            self.assertEqual(csv[2], instance.name)
            self.assertEqual(csv[8], instance.slot_id)

        for fsu in ("gpubaseboard", "cpu", "disk", "fan", "mainboard", "otherfsu"):
            with self.subTest(fsu=fsu):
                instance = self.fsu_models[fsu](
                    fsu_type=self.fsu_types[fsu],
                    device=self.device,
                    name="test_fsu",
                    status=Status.objects.get(slug="active"),
                )
                instance.save()

                columns = 13 if fsu in ["cpu", "disk"] else 12
                csv = instance.to_csv()
                self.assertIsInstance(csv, tuple)
                self.assertEqual(len(csv), columns)
                self.assertEqual(csv[2], instance.name)

    def test_fsu_move_to_device(self):
        """Ensure when a device is set on an FSU, the storage_location is cleared."""
        for fsu, model in self.fsu_models.items():
            with self.subTest(fsu=fsu):
                instance = model(
                    fsu_type=self.fsu_types[fsu],
                    location=self.location,
                    name="test_fsu",
                    status=Status.objects.get(slug="available"),
                )
                instance.save()

                self.assertEqual(instance.parent, self.location)
                self.assertIsNone(instance.device)

                instance.device = self.device
                instance.save()

                self.assertIsNotNone(instance.device)
                self.assertIsNone(instance.location)

    def test_fsu_duplicate_names(self):
        """Verify unique name constraints for FSUs in the same device or storage location."""
        for fsu, model in self.fsu_models.items():
            with self.subTest(fsu=fsu):
                instance1 = model(
                    fsu_type=self.fsu_types[fsu],
                    device=self.device,
                    name="test_fsu",
                    status=Status.objects.get(slug="active"),
                )
                instance1.save()

                instance2 = model(
                    fsu_type=self.fsu_types[fsu],
                    device=self.device,
                    name=instance1.name,
                    status=Status.objects.get(slug="active"),
                )

                # Two FSUs with the same name in the same device should fail validation.
                with self.assertRaises(ValidationError):
                    instance2.full_clean()

                # Two FSUs with the same name, but in different devices should pass validation.
                instance1.device = Device.objects.last()
                instance1.save()
                instance2.full_clean()

                # Two FSUs with the same name in the same storage location should fail validation.
                instance1.device = None
                instance1.location = self.location
                instance1.status = Status.objects.get(name="Available")
                instance1.save()
                instance2.device = None
                instance2.location = self.location
                instance2.status = Status.objects.get(name="Available")
                with self.assertRaises(ValidationError):
                    instance2.full_clean()

                # Two FSUs with the same name, but in different storage locations
                # should pass validation.
                instance1.location = Location.objects.last()
                instance1.save()
                instance2.full_clean()
                instance2.save()

    def test_fsu_incorrect_type(self):
        """Verify validation of the correct FSU type on FSU creation."""
        fsu_type = models.OtherFSUType(
            manufacturer=Manufacturer.objects.first(),
            name="Generic FSU",
            part_number="0002",
        )
        fsu_type.save()

        with self.assertRaises(ValueError):
            _ = models.GPU(
                fsu_type=fsu_type,
                device=self.device,
                name="test_gpu",
                status=Status.objects.get(slug="active"),
            )
