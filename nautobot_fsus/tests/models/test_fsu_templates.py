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
from nautobot.dcim.models import Device

from nautobot_fsus import models
from nautobot_fsus.utilities.testing import NautobotFSUModelTestCases


class CPUTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the CPUTemplate model."""

    template_model = models.CPUTemplate
    type_model = models.CPUType
    target_model = models.CPU

    def test_instantiate_with_bad_parent(self):
        """Validate that instantiating an FSU with a bad parent fails."""
        template = self.template_model.objects.create(
            device_type=self.device_type,
            name="bad_template",
            fsu_type=self.fsu_type,
        )

        with self.assertRaises(NotImplementedError):
            # This is explicitly calling a non-direct parent class for the purpose
            # of getting the base method defined in FSUTemplateModel.
            # pylint: disable=bad-super-call
            _ = super(models.CPUTemplate, template).instantiate(
                device=Device.objects.first(),
            )


class DiskTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the DiskTemplate model."""

    template_model = models.DiskTemplate
    type_model = models.DiskType
    target_model = models.Disk


class FanTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the FanTemplate model."""

    template_model = models.FanTemplate
    type_model = models.FanType
    target_model = models.Fan


class GPUTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the GPUTemplate model."""

    template_model = models.GPUTemplate
    type_model = models.GPUType
    target_model = models.GPU


class GPUBaseboardTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the GPUBaseboardTemplate model."""

    template_model = models.GPUBaseboardTemplate
    type_model = models.GPUBaseboardType
    target_model = models.GPUBaseboard


class HBATemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the HBATemplate model."""

    template_model = models.HBATemplate
    type_model = models.HBAType
    target_model = models.HBA


class MainboardTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the MainboardTemplate model."""

    template_model = models.MainboardTemplate
    type_model = models.MainboardType
    target_model = models.Mainboard


class NICTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the NICTemplate model."""

    template_model = models.NICTemplate
    type_model = models.NICType
    target_model = models.NIC


class OtherFSUTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the OtherFSUTemplate model."""

    template_model = models.OtherFSUTemplate
    type_model = models.OtherFSUType
    target_model = models.OtherFSU


class PSUTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the PSUTemplate model."""

    template_model = models.PSUTemplate
    type_model = models.PSUType
    target_model = models.PSU


class RAMModuleTemplateTestCase(NautobotFSUModelTestCases.FSUTemplateTestCase):
    """Tests for the RAMModuleTemplate model."""

    template_model = models.RAMModuleTemplate
    type_model = models.RAMModuleType
    target_model = models.RAMModule
