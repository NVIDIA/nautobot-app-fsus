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

"""Tests for forms defined in the Nautobot FSUs app."""
from nautobot.dcim.models import Manufacturer

from nautobot_fsus import forms, models
from nautobot_fsus.utilities.testing import FSUFormTestCases


class CPUTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for CPU forms."""

    model = models.CPU
    type_model = models.CPUType
    form_model = forms.CPUForm
    bulk_form_model = forms.CPUBulkEditForm
    filter_form_model = forms.CPUFilterForm
    csv_form_model = forms.CPUCSVForm


class CPUTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for CPUTemplate forms."""

    model = models.CPUTemplate
    type_model = models.CPUType
    form_model = forms.CPUTemplateForm
    bulk_form_model = forms.CPUTemplateBulkEditForm
    create_form_model = forms.CPUTemplateCreateForm


class CPUTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for CPUType forms."""

    type_model = models.CPUType
    form_model = forms.CPUTypeForm
    bulk_form_model = forms.CPUTypeBulkEditForm
    filter_form_model = forms.CPUTypeFilterForm

    def test_new_fsu_type(self):
        """Test adding a new CPU type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "Z0101",
                "architecture": "arm",
                "cpu_speed": 1.9,
                "cores": 32,
                "pcie_generation": 0,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class DiskTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for Disk forms."""

    model = models.Disk
    type_model = models.DiskType
    form_model = forms.DiskForm
    bulk_form_model = forms.DiskBulkEditForm
    filter_form_model = forms.DiskFilterForm
    csv_form_model = forms.DiskCSVForm


class DiskTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for Disk templates."""

    model = models.DiskTemplate
    type_model = models.DiskType
    form_model = forms.DiskTemplateForm
    bulk_form_model = forms.DiskTemplateBulkEditForm
    create_form_model = forms.DiskTemplateCreateForm


class DiskTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for Disk type."""

    type_model = models.DiskType
    form_model = forms.DiskTypeForm
    bulk_form_model = forms.DiskTypeBulkEditForm
    filter_form_model = forms.DiskTypeFilterForm

    def test_new_fsu_type(self):
        """Test adding a new Disk type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "Z0101",
                "disk_type": "SSD",
                "size": 256,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class FanTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for Fan forms."""

    model = models.Fan
    type_model = models.FanType
    form_model = forms.FanForm
    bulk_form_model = forms.FanBulkEditForm
    filter_form_model = forms.FanFilterForm
    csv_form_model = forms.FanCSVForm


class FanTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for Fan templates."""

    model = models.FanTemplate
    type_model = models.FanType
    form_model = forms.FanTemplateForm
    bulk_form_model = forms.FanTemplateBulkEditForm
    create_form_model = forms.FanTemplateCreateForm


class FanTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for Fan type."""

    type_model = models.FanType
    form_model = forms.FanTypeForm
    bulk_form_model = forms.FanTypeBulkEditForm
    filter_form_model = forms.FanTypeFilterForm


class GPUTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for GPU forms."""

    model = models.GPU
    type_model = models.GPUType
    form_model = forms.GPUForm
    bulk_form_model = forms.GPUBulkEditForm
    filter_form_model = forms.GPUFilterForm
    csv_form_model = forms.GPUCSVForm


class GPUTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for GPU templates."""

    model = models.GPUTemplate
    type_model = models.GPUType
    form_model = forms.GPUTemplateForm
    bulk_form_model = forms.GPUTemplateBulkEditForm
    create_form_model = forms.GPUTemplateCreateForm


class GPUTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for GPU type."""

    type_model = models.GPUType
    form_model = forms.GPUTypeForm
    bulk_form_model = forms.GPUTypeBulkEditForm
    filter_form_model = forms.GPUTypeFilterForm


class GPUBaseboardTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for GPUBaseboard forms."""

    model = models.GPUBaseboard
    type_model = models.GPUBaseboardType
    form_model = forms.GPUBaseboardForm
    bulk_form_model = forms.GPUBaseboardBulkEditForm
    filter_form_model = forms.GPUBaseboardFilterForm
    csv_form_model = forms.GPUBaseboardCSVForm


class GPUBaseboardTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for GPUBaseboard templates."""

    model = models.GPUBaseboardTemplate
    type_model = models.GPUBaseboardType
    form_model = forms.GPUBaseboardTemplateForm
    bulk_form_model = forms.GPUBaseboardTemplateBulkEditForm
    create_form_model = forms.GPUBaseboardTemplateCreateForm


class GPUBaseboardTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for GPUBaseboard type."""

    type_model = models.GPUBaseboardType
    form_model = forms.GPUBaseboardTypeForm
    bulk_form_model = forms.GPUBaseboardTypeBulkEditForm
    filter_form_model = forms.GPUBaseboardTypeFilterForm

    def test_new_fsu_type(self):
        """Test adding a new Baseboard type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "Z0101",
                "slot_count": 8,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class HBATestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for HBA forms."""

    model = models.HBA
    type_model = models.HBAType
    form_model = forms.HBAForm
    bulk_form_model = forms.HBABulkEditForm
    filter_form_model = forms.HBAFilterForm
    csv_form_model = forms.HBACSVForm


class HBATemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for HBA templates."""

    model = models.HBATemplate
    type_model = models.HBAType
    form_model = forms.HBATemplateForm
    bulk_form_model = forms.HBATemplateBulkEditForm
    create_form_model = forms.HBATemplateCreateForm


class HBATypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for HBA type."""

    type_model = models.HBAType
    form_model = forms.HBATypeForm
    bulk_form_model = forms.HBATypeBulkEditForm
    filter_form_model = forms.HBATypeFilterForm


class MainboardTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for Mainboard forms."""

    model = models.Mainboard
    type_model = models.MainboardType
    form_model = forms.MainboardForm
    bulk_form_model = forms.MainboardBulkEditForm
    filter_form_model = forms.MainboardFilterForm
    csv_form_model = forms.MainboardCSVForm


class MainboardTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for Mainboard templates."""

    model = models.MainboardTemplate
    type_model = models.MainboardType
    form_model = forms.MainboardTemplateForm
    bulk_form_model = forms.MainboardTemplateBulkEditForm
    create_form_model = forms.MainboardTemplateCreateForm


class MainboardTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for Mainboard type."""

    type_model = models.MainboardType
    form_model = forms.MainboardTypeForm
    bulk_form_model = forms.MainboardTypeBulkEditForm
    filter_form_model = forms.MainboardTypeFilterForm

    def test_new_fsu_type(self):
        """Test adding a new Mainboard type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "Z0101",
                "cpu_socket_count": 2,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class NICTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for NIC forms."""

    model = models.NIC
    type_model = models.NICType
    form_model = forms.NICForm
    bulk_form_model = forms.NICBulkEditForm
    filter_form_model = forms.NICFilterForm
    csv_form_model = forms.NICCSVForm


class NICTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for NIC templates."""

    model = models.NICTemplate
    type_model = models.NICType
    form_model = forms.NICTemplateForm
    bulk_form_model = forms.NICTemplateBulkEditForm
    create_form_model = forms.NICTemplateCreateForm


class NICTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for NIC type."""

    type_model = models.NICType
    form_model = forms.NICTypeForm
    bulk_form_model = forms.NICTypeBulkEditForm
    filter_form_model = forms.NICTypeFilterForm

    def test_new_nic_type(self):
        """Test adding a new NIC type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "Z0101",
                "interface_count": 2,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())


class OtherFSUTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for OtherFSU forms."""

    model = models.OtherFSU
    type_model = models.OtherFSUType
    form_model = forms.OtherFSUForm
    bulk_form_model = forms.OtherFSUBulkEditForm
    filter_form_model = forms.OtherFSUFilterForm
    csv_form_model = forms.OtherFSUCSVForm


class OtherFSUTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for OtherFSU templates."""

    model = models.OtherFSUTemplate
    type_model = models.OtherFSUType
    form_model = forms.OtherFSUTemplateForm
    bulk_form_model = forms.OtherFSUTemplateBulkEditForm
    create_form_model = forms.OtherFSUTemplateCreateForm


class OtherFSUTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for OtherFSU type."""

    type_model = models.OtherFSUType
    form_model = forms.OtherFSUTypeForm
    bulk_form_model = forms.OtherFSUTypeBulkEditForm
    filter_form_model = forms.OtherFSUTypeFilterForm


class PSUTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for PSU forms."""

    model = models.PSU
    type_model = models.PSUType
    form_model = forms.PSUForm
    bulk_form_model = forms.PSUBulkEditForm
    filter_form_model = forms.PSUFilterForm
    csv_form_model = forms.PSUCSVForm


class PSUTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for PSU templates."""

    model = models.PSUTemplate
    type_model = models.PSUType
    form_model = forms.PSUTemplateForm
    bulk_form_model = forms.PSUTemplateBulkEditForm
    create_form_model = forms.PSUTemplateCreateForm


class PSUTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for PSU type."""

    type_model = models.PSUType
    form_model = forms.PSUTypeForm
    bulk_form_model = forms.PSUTypeBulkEditForm
    filter_form_model = forms.PSUTypeFilterForm


class RAMModuleTestCase(FSUFormTestCases.FSUModelFormTestCase):
    """Tests for RAMModule forms."""

    model = models.RAMModule
    type_model = models.RAMModuleType
    form_model = forms.RAMModuleForm
    bulk_form_model = forms.RAMModuleBulkEditForm
    filter_form_model = forms.RAMModuleFilterForm
    csv_form_model = forms.RAMModuleCSVForm


class RAMModuleTemplateTestCase(FSUFormTestCases.FSUTemplateFormTestCase):
    """Tests for RAMModule templates."""

    model = models.RAMModuleTemplate
    type_model = models.RAMModuleType
    form_model = forms.RAMModuleTemplateForm
    bulk_form_model = forms.RAMModuleTemplateBulkEditForm
    create_form_model = forms.RAMModuleTemplateCreateForm


class RAMModuleTypeTestCase(FSUFormTestCases.FSUTypeFormTestCase):
    """Tests for RAMModule type."""

    type_model = models.RAMModuleType
    form_model = forms.RAMModuleTypeForm
    bulk_form_model = forms.RAMModuleTypeBulkEditForm
    filter_form_model = forms.RAMModuleTypeFilterForm

    def test_new_fsu_type(self):
        """Test adding a new FSU type."""
        form = self.form_model(
            data={
                "manufacturer": Manufacturer.objects.first(),
                "name": f"Test {self.instance_model}",
                "part_number": "X0001Z",
                "module_type": "u",
                "technology": "ddr5",
                "speed": 3200,
                "capacity": 32,
                "quantity": 1,
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
