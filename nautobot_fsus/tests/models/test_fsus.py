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
from nautobot.dcim.models import Interface, PowerPort
from nautobot.extras.models import Status

from nautobot_fsus import models
from nautobot_fsus.utilities.testing import NautobotFSUModelTestCases


class CPUTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the CPU model."""

    model = models.CPU
    type_model = models.CPUType
    parent_model = models.Mainboard
    parent_model_type = models.MainboardType
    parent_field = "parent_mainboard"

    def test_parent_socket_count(self):
        """Test that assigning more CPUs than available sockets fails."""
        parent_type = models.MainboardType(
            manufacturer=self.manufacturer,
            name="Test Mainboard",
            part_number="x1",
            cpu_socket_count=2,
        )
        parent_type.save()

        parent = models.Mainboard(
            fsu_type=parent_type,
            device=self.device,
            name="Test Mainboard",
            status=self.status,
        )
        parent.save()

        _ = models.CPU.objects.create(
            fsu_type=self.fsu_type,
            device=self.device,
            name="cpu_0",
            status=self.status,
            parent_mainboard=parent,
        )
        _ = models.CPU.objects.create(
            fsu_type=self.fsu_type,
            device=self.device,
            name="cpu_1",
            status=self.status,
            parent_mainboard=parent,
        )

        instance = models.CPU(
            fsu_type=self.fsu_type,
            device=self.device,
            name="cpu_2",
            status=self.status,
            parent_mainboard=parent,
        )
        with self.assertRaises(ValidationError) as context:
            instance.full_clean()
        error = context.exception
        self.assertEqual(error.messages[0], "Mainboard has no available CPU sockets.")


class DiskTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the Disk model."""

    model = models.Disk
    type_model = models.DiskType
    parent_model = models.HBA
    parent_model_type = models.HBAType
    parent_field = "parent_hba"


class FanTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the Fan model."""

    model = models.Fan
    type_model = models.FanType


class GPUTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the GPU model."""

    model = models.GPU
    type_model = models.GPUType
    parent_model = models.GPUBaseboard
    parent_model_type = models.GPUBaseboardType
    parent_field = "parent_gpubaseboard"

    def test_parent_slot_count(self):
        """Test that assigning more GPUs than available slots fails."""
        parent_type = models.GPUBaseboardType(
            manufacturer=self.manufacturer,
            name="Test Baseboard",
            part_number="x1",
            slot_count=2,
        )
        parent_type.save()

        parent = models.GPUBaseboard(
            fsu_type=parent_type,
            device=self.device,
            name="Test Baseboard",
            status=self.status,
        )
        parent.save()

        _ = models.GPU.objects.create(
            fsu_type=self.fsu_type,
            device=self.device,
            name="gpu_0",
            status=self.status,
            parent_gpubaseboard=parent,
        )
        _ = models.GPU.objects.create(
            fsu_type=self.fsu_type,
            device=self.device,
            name="gpu_1",
            status=self.status,
            parent_gpubaseboard=parent,
        )

        instance = models.GPU(
            fsu_type=self.fsu_type,
            device=self.device,
            name="gpu_2",
            status=self.status,
            parent_gpubaseboard=parent,
        )
        with self.assertRaises(ValidationError) as context:
            instance.full_clean()
        error = context.exception
        self.assertEqual(error.messages[0], "GPU Baseboard has no available slots.")


class GPUBaseboardTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the GPUBaseboard model."""

    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType
    child_model = models.GPU
    child_model_type = models.GPUType
    child_field = "gpus"


class HBATestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the HBA model."""

    model = models.HBA
    type_model = models.HBAType
    child_model = models.Disk
    child_model_type = models.DiskType
    child_field = "disks"


class MainboardTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the Mainboard model."""

    model = models.Mainboard
    type_model = models.MainboardType
    child_model = models.CPU
    child_model_type = models.CPUType
    child_field = "cpus"


class NICTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the NIC model."""

    model = models.NIC
    type_model = models.NICType

    def test_child_interfaces(self):
        """Test assigning child interfaces to a NIC."""
        interface = Interface.objects.create(
            device=self.device,
            name="eth0",
            type="1000base-x-gbic",
            status=Status.objects.get_for_model(Interface).first(),
        )

        instance = models.NIC(
            fsu_type=self.fsu_type,
            device=self.device,
            name="Test NIC",
            status=self.status,
        )
        instance.save()
        instance.interfaces.set([interface])
        instance.validated_save()

        self.assertEqual(interface.parent_nic.first(), instance)


class OtherFSUTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the OtherFSU model."""

    model = models.OtherFSU
    type_model = models.OtherFSUType


class PSUTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the PSU model."""

    model = models.PSU
    type_model = models.PSUType

    def test_child_power_ports(self):
        """Test assigning child power ports to a PSU."""
        power_port = PowerPort.objects.create(
            device=self.device,
            name="PPort1",
        )

        instance = models.PSU(
            fsu_type=self.fsu_type,
            device=self.device,
            name="Test PSU",
            status=self.status,
        )
        instance.save()
        instance.power_ports.set([power_port])
        instance.validated_save()
        self.assertEqual(power_port.parent_psu.first(), instance)


class RAMModuleTestCase(NautobotFSUModelTestCases.FSUTestCase):
    """Tests for the RAMModule model."""

    model = models.RAMModule
    type_model = models.RAMModuleType
