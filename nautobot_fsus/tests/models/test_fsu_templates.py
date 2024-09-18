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

"""Tests for FSU Template models defined by the Nautobot FSUS app."""
from time import sleep

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot.extras.models import CustomField, Status

from nautobot_fsus import models


class FSUTemplateTestCase(TestCase):
    """Test case for FSU templates."""

    @classmethod
    def setUpTestData(cls):
        """Set up the base device type for the tests."""
        manufacturers = [Manufacturer.objects.first(), Manufacturer.objects.last()]

        cls.device_type = DeviceType.objects.create(
            manufacturer=manufacturers[0],
            model="Test Device Type",
            slug="test_device_type",
        )

        cls.fsu_types = {
            "cpu": models.CPUType.objects.create(
                manufacturer=manufacturers[0],
                name="Master Control",
                part_number="0001",
            ),
            "disk": models.DiskType.objects.create(
                manufacturer=manufacturers[0],
                name="Infinite Data",
                part_number="0001",
            ),
            "fan": models.FanType.objects.create(
                manufacturer=manufacturers[0],
                name="Wind Tunnel",
                part_number="0001",
            ),
            "gpu": models.GPUType.objects.create(
                manufacturer=manufacturers[0],
                name="AI Cruncher",
                part_number="0001",
            ),
            "gpubaseboard": models.GPUBaseboardType.objects.create(
                manufacturer=manufacturers[0],
                name="GPU Farm",
                part_number="0001",
            ),
            "hba": models.HBAType.objects.create(
                manufacturer=manufacturers[0],
                name="Storage Tentacles",
                part_number="0001",
            ),
            "mainboard": models.MainboardType.objects.create(
                manufacturer=manufacturers[0],
                name="The One Ring To Rule Them All",
                part_number="0001",
            ),
            "nic": models.NICType.objects.create(
                manufacturer=manufacturers[1],
                name="Packet Spitter",
                part_number="0001",
            ),
            "otherfsu": models.OtherFSUType.objects.create(
                manufacturer=manufacturers[1],
                name="Mystery Box",
                part_number="0001",
            ),
            "psu": models.PSUType.objects.create(
                manufacturer=manufacturers[0],
                name="Juice Monster",
                part_number="0001",
            ),
            "rammodule": models.RAMModuleType.objects.create(
                manufacturer=manufacturers[0],
                name="Vast Sea of RAM",
                part_number="0001",
                capacity=64,
            ),
        }

        cls.fsu_templates = {
            "cpu": models.CPUTemplate,
            "disk": models.DiskTemplate,
            "fan": models.FanTemplate,
            "gpu": models.GPUTemplate,
            "gpubaseboard": models.GPUBaseboardTemplate,
            "hba": models.HBATemplate,
            "mainboard": models.MainboardTemplate,
            "nic": models.NICTemplate,
            "otherfsu": models.OtherFSUTemplate,
            "psu": models.PSUTemplate,
            "rammodule": models.RAMModuleTemplate,
        }

    def test_fsutemplate_basics(self):
        """Test common parts of the FSU template model."""
        for fsu, model in self.fsu_templates.items():
            with self.subTest(fsu=fsu):
                template = model.objects.create(
                    device_type=self.device_type,
                    name="test_fsu",
                    fsu_type=self.fsu_types[fsu],
                )

            # Only test this once.
            if fsu == "gpu":
                with self.assertRaises(NotImplementedError):
                    # This is explicitly calling a non-direct parent class for the purpose
                    # of getting the base method defined in FSUTemplateModel.
                    # pylint: disable=bad-super-call
                    _ = super(models.GPUTemplate, template).instantiate(
                        device=Device.objects.first(),
                    )

            object_change = template.to_objectchange("create")
            self.assertEqual(object_change.changed_object_type.model_class(), template._meta.model)
            self.assertEqual(object_change.changed_object_id, template.id)
            self.assertEqual(
                object_change.related_object_type.model_class(),
                template.device_type._meta.model,
            )
            self.assertEqual(object_change.related_object_id, template.device_type.id)

    def test_create_and_assign_templates(self):
        """Validate creation of templates and associating them with DeviceTypes."""
        cpu_template = models.CPUTemplate.objects.create(
            device_type=self.device_type,
            name="CPU 0",
            fsu_type=self.fsu_types["cpu"],
        )
        disk_template = models.DiskTemplate.objects.create(
            device_type=self.device_type,
            name="sda",
            fsu_type=self.fsu_types["disk"],
        )
        fan_template = models.FanTemplate.objects.create(
            device_type=self.device_type,
            name="Fan 0",
            fsu_type=self.fsu_types["fan"],
        )
        gpu_template = models.GPUTemplate.objects.create(
            device_type=self.device_type,
            name="gpu_0",
            fsu_type=self.fsu_types["gpu"],
            pci_slot_id="00000000:07:00.0",
        )
        gpubaseboard_template = models.GPUBaseboardTemplate.objects.create(
            device_type=self.device_type,
            name="GPU Baseboard 0",
            fsu_type=self.fsu_types["gpubaseboard"],
        )
        hba_template = models.HBATemplate.objects.create(
            device_type=self.device_type,
            name="HBA 0",
            fsu_type=self.fsu_types["hba"],
            pci_slot_id="00000000:08:00.0",
        )
        mainboard_template = models.MainboardTemplate.objects.create(
            device_type=self.device_type,
            name="MB",
            fsu_type=self.fsu_types["mainboard"],
        )
        nic_template = models.NICTemplate.objects.create(
            device_type=self.device_type,
            name="NIC0",
            fsu_type=self.fsu_types["nic"],
            pci_slot_id="00000000:09:00.0",
        )
        otherfsu_template = models.OtherFSUTemplate.objects.create(
            device_type=self.device_type,
            name="BlackBox",
            fsu_type=self.fsu_types["otherfsu"],
        )
        psu_template1 = models.PSUTemplate.objects.create(
            device_type=self.device_type,
            name="PSU00",
            fsu_type=self.fsu_types["psu"],
            redundant=True,
        )
        psu_template2 = models.PSUTemplate.objects.create(
            device_type=self.device_type,
            name="PSU01",
            fsu_type=self.fsu_types["psu"],
            redundant=True,
        )
        rammodule_template = models.RAMModuleTemplate.objects.create(
            device_type=self.device_type,
            name="dimm_a1",
            fsu_type=self.fsu_types["rammodule"],
            slot_id="A1",
        )

        self.assertEqual(self.device_type.cputemplates.count(), 1)
        self.assertEqual(self.device_type.rammoduletemplates.count(), 1)
        self.assertEqual(self.device_type.disktemplates.count(), 1)
        self.assertEqual(self.device_type.fantemplates.count(), 1)
        self.assertEqual(self.device_type.gpubaseboardtemplates.count(), 1)
        self.assertEqual(self.device_type.gputemplates.count(), 1)
        self.assertEqual(self.device_type.hbatemplates.count(), 1)
        self.assertEqual(self.device_type.mainboardtemplates.count(), 1)
        self.assertEqual(self.device_type.nictemplates.count(), 1)
        self.assertEqual(self.device_type.psutemplates.count(), 2)
        self.assertEqual(self.device_type.otherfsutemplates.count(), 1)

        self.assertEqual(self.device_type.cputemplates.first().name, cpu_template.name)
        self.assertEqual(self.device_type.rammoduletemplates.first().name, rammodule_template.name)
        self.assertEqual(self.device_type.rammoduletemplates.first().slot_id, "A1")
        self.assertEqual(self.device_type.disktemplates.first().name, disk_template.name)
        self.assertEqual(self.device_type.fantemplates.first().name, fan_template.name)
        self.assertEqual(
            self.device_type.gpubaseboardtemplates.first().name,
            gpubaseboard_template.name
        )
        self.assertEqual(self.device_type.gputemplates.first().name, gpu_template.name)
        self.assertEqual(self.device_type.hbatemplates.first().name, hba_template.name)
        self.assertEqual(self.device_type.mainboardtemplates.first().name, mainboard_template.name)
        self.assertEqual(self.device_type.nictemplates.first().name, nic_template.name)
        self.assertEqual(self.device_type.psutemplates.first().name, psu_template1.name)
        self.assertEqual(self.device_type.psutemplates.last().name, psu_template2.name)
        self.assertTrue(self.device_type.psutemplates.last().redundant)
        self.assertEqual(self.device_type.otherfsutemplates.first().name, otherfsu_template.name)

    def test_instantiate_devices_fsus(self):
        """Validate creation of FSUs for new Devices, including custom and FSU fields."""
        # pylint: disable=too-many-locals,too-many-statements

        custom_fields = [
            CustomField.objects.create(
                type=CustomFieldTypeChoices.TYPE_TEXT,
                name="cf_field_1",
                default="value_1",
            ),
            CustomField.objects.create(
                type=CustomFieldTypeChoices.TYPE_INTEGER,
                name="cf_field_2",
                default=42,
            ),
            CustomField.objects.create(
                type=CustomFieldTypeChoices.TYPE_BOOLEAN,
                name="cf_field_3",
                default=False,
            ),
            CustomField.objects.create(
                type=CustomFieldTypeChoices.TYPE_DATE,
                name="cf_field_4",
                default="1970-01-01",
            )
        ]
        custom_fields[0].content_types.set(
            [
                ContentType.objects.get_for_model(models.CPU),
                ContentType.objects.get_for_model(models.Disk),
                ContentType.objects.get_for_model(models.Fan),
            ]
        )
        custom_fields[1].content_types.set(
            [
                ContentType.objects.get_for_model(models.GPU),
                ContentType.objects.get_for_model(models.GPUBaseboard),
                ContentType.objects.get_for_model(models.HBA),
            ]
        )
        custom_fields[2].content_types.set(
            [
                ContentType.objects.get_for_model(models.Mainboard),
                ContentType.objects.get_for_model(models.NIC),
                ContentType.objects.get_for_model(models.OtherFSU)
            ]
        )
        custom_fields[3].content_types.set(
            [
                ContentType.objects.get_for_model(models.PSU),
                ContentType.objects.get_for_model(models.RAMModule),
            ]
        )

        cpu_template = models.CPUTemplate.objects.create(
            device_type=self.device_type,
            name="CPU 0",
            fsu_type=self.fsu_types["cpu"],
        )
        rammodule_template = models.RAMModuleTemplate.objects.create(
            device_type=self.device_type,
            name="dimm_a1",
            fsu_type=self.fsu_types["rammodule"],
            slot_id="A1",
        )
        disk_template = models.DiskTemplate.objects.create(
            device_type=self.device_type,
            name="sda",
            fsu_type=self.fsu_types["disk"],
        )
        fan_template = models.FanTemplate.objects.create(
            device_type=self.device_type,
            name="Fan 0",
            fsu_type=self.fsu_types["fan"],
        )
        gpu_template = models.GPUTemplate.objects.create(
            device_type=self.device_type,
            name="gpu_0",
            fsu_type=self.fsu_types["gpu"],
            pci_slot_id="00000000:07:00.0",
        )
        gpubaseboard_template = models.GPUBaseboardTemplate.objects.create(
            device_type=self.device_type,
            name="GPU Baseboard 0",
            fsu_type=self.fsu_types["gpubaseboard"],
        )
        hba_template = models.HBATemplate.objects.create(
            device_type=self.device_type,
            name="HBA 0",
            fsu_type=self.fsu_types["hba"],
            pci_slot_id="00000000:08:00.0",
        )
        mainboard_template = models.MainboardTemplate.objects.create(
            device_type=self.device_type,
            name="MB",
            fsu_type=self.fsu_types["mainboard"],
        )
        nic_template = models.NICTemplate.objects.create(
            device_type=self.device_type,
            name="NIC0",
            fsu_type=self.fsu_types["nic"],
            pci_slot_id="00000000:09:00.0",
        )
        psu_template = models.PSUTemplate.objects.create(
            device_type=self.device_type,
            name="PSU00",
            fsu_type=self.fsu_types["psu"],
        )
        otherfsu_template = models.OtherFSUTemplate.objects.create(
            device_type=self.device_type,
            name="BlackBox",
            fsu_type=self.fsu_types["otherfsu"],
        )

        device = Device.objects.create(
            device_type=self.device_type,
            device_role=DeviceRole.objects.first(),
            status=Status.objects.get_for_model(Device).first(),
            name="Device X",
            site=Site.objects.first(),
        )

        # Pause for the signal
        sleep(1)

        cpu = device.cpus.first()
        self.assertIsNotNone(cpu)
        self.assertEqual(cpu.name, cpu_template.name)
        self.assertEqual(cpu.cf["cf_field_1"], custom_fields[0].default)
        self.assertEqual(len(cpu.get_fsu_fields()), 1)

        disk = device.disks.first()
        self.assertIsNotNone(disk)
        self.assertEqual(disk.name, disk_template.name)
        self.assertEqual(disk.cf["cf_field_1"], custom_fields[0].default)
        self.assertEqual(len(disk.get_fsu_fields()), 1)

        fan = device.fans.first()
        self.assertIsNotNone(fan)
        self.assertEqual(fan.name, fan_template.name)
        self.assertEqual(fan.cf["cf_field_1"], custom_fields[0].default)
        self.assertEqual(len(fan.get_fsu_fields()), 1)

        gpu = device.gpus.first()
        self.assertIsNotNone(gpu)
        self.assertEqual(gpu.name, gpu_template.name)
        self.assertEqual(gpu.pci_slot_id, gpu_template.pci_slot_id)
        self.assertEqual(gpu.cf["cf_field_2"], custom_fields[1].default)
        self.assertEqual(len(gpu.get_fsu_fields()), 1)

        gpubaseboard = device.gpubaseboards.first()
        self.assertIsNotNone(gpubaseboard)
        self.assertEqual(gpubaseboard.name, gpubaseboard_template.name)
        self.assertEqual(gpubaseboard.cf["cf_field_2"], custom_fields[1].default)
        self.assertEqual(len(gpubaseboard.get_fsu_fields()), 1)

        hba = device.hbas.first()
        self.assertIsNotNone(hba)
        self.assertEqual(hba.name, hba_template.name)
        self.assertEqual(hba.pci_slot_id, hba_template.pci_slot_id)
        self.assertEqual(hba.cf["cf_field_2"], custom_fields[1].default)
        self.assertEqual(hba.field_data["fsu_field_2"], fsu_fields[1].default)
        self.assertEqual(len(hba.get_fsu_fields()), 1)

        mainboard = device.mainboards.first()
        self.assertIsNotNone(mainboard)
        self.assertEqual(mainboard.name, mainboard_template.name)
        self.assertEqual(mainboard.cf["cf_field_3"], custom_fields[2].default)
        self.assertEqual(len(mainboard.get_fsu_fields()), 1)

        nic = device.nics.first()
        self.assertIsNotNone(nic)
        self.assertEqual(nic.name, nic_template.name)
        self.assertEqual(nic.pci_slot_id, nic_template.pci_slot_id)
        self.assertEqual(nic.cf["cf_field_3"], custom_fields[2].default)
        self.assertEqual(len(nic.get_fsu_fields()), 1)

        otherfsu = device.otherfsus.first()
        self.assertIsNotNone(otherfsu)
        self.assertEqual(otherfsu.name, otherfsu_template.name)
        self.assertEqual(otherfsu.cf["cf_field_3"], custom_fields[2].default)
        self.assertEqual(len(otherfsu.get_fsu_fields()), 1)

        psu = device.psus.first()
        self.assertIsNotNone(psu)
        self.assertEqual(psu.name, psu_template.name)
        self.assertEqual(psu.redundant, psu_template.redundant)
        self.assertEqual(psu.cf["cf_field_4"], custom_fields[3].default)
        self.assertEqual(len(psu.get_fsu_fields()), 1)

        rammodule = device.rammodules.first()
        self.assertIsNotNone(rammodule)
        self.assertEqual(rammodule.name, rammodule_template.name)
        self.assertEqual(rammodule.cf["cf_field_4"], custom_fields[3].default)
        self.assertEqual(len(rammodule.get_fsu_fields()), 1)
