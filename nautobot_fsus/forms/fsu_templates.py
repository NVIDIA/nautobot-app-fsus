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

"""Form definitions for FSU template models."""
from django import forms
from nautobot.extras.forms import NautobotBulkEditForm
from nautobot.utilities.forms.fields import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
    ExpandableNameField,
)

from nautobot_fsus import models
from nautobot_fsus.forms.mixins import (
    FSUTemplateCSVForm,
    FSUTemplateCreateForm,
    FSUTemplateModelForm,
    FSUTemplatePCIModelCreateForm,
)


class CPUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing CPUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.CPUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.CPUType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """CPUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class CPUTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of CPUTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.CPUType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="CPU type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """CPUTemplateCSVForm model options."""

        model = models.CPUTemplate


class CPUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more CPUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateCreateForm.Meta):
        """CPUTemplateCreateForm model options."""

        model = models.CPUTemplate


class CPUTemplateForm(FSUTemplateModelForm):
    """Form for updating a CPUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """CPUTemplateForm model options."""

        model = models.CPUTemplate


class DiskTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing DiskTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.DiskTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.DiskType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """DiskTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class DiskTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of DiskTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.DiskType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="Disk type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """DiskTemplateCSVForm model options."""

        model = models.DiskTemplate


class DiskTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more DiskTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """DiskTemplateCreateForm model options."""

        model = models.DiskTemplate


class DiskTemplateForm(FSUTemplateModelForm):
    """Form for updating a DiskTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """DiskTemplateForm model options."""

        model = models.DiskTemplate


class FanTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing FanTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.FanTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.FanType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """FanTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class FanTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of FanTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.FanType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="Fan type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """FanTemplateCSVForm model options."""

        model = models.FanTemplate


class FanTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more FanTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateCreateForm.Meta):
        """FanTemplateCreateForm model options."""

        model = models.FanTemplate


class FanTemplateForm(FSUTemplateModelForm):
    """Form for updating a FanTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """FanTemplateForm model options."""

        model = models.FanTemplate


class GPUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing GPUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.GPUType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """GPUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class GPUTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of GPUTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.GPUType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="GPU type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """GPUTemplateCSVForm model options."""

        model = models.GPUTemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class GPUTemplateCreateForm(FSUTemplatePCIModelCreateForm):
    """Form for creating one or more GPUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplatePCIModelCreateForm.Meta):
        """GPUTemplateCreateForm model options."""

        model = models.GPUTemplate


class GPUTemplateForm(FSUTemplateModelForm):
    """Form for updating a GPUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """GPUTemplateForm model options."""

        model = models.GPUTemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class GPUBaseboardTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing GPUBaseboardTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUBaseboardTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """GPUBaseboardTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class GPUBaseboardTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of GPUBaseboardTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="GPUBaseboard type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """GPUBaseboardTemplateCSVForm model options."""

        model = models.GPUBaseboardTemplate


class GPUBaseboardTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more GPUBaseboardTemplate instances."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        label="FSU Type",
    )

    class Meta(FSUTemplateCreateForm.Meta):
        """GPUBaseboardTemplateCreateForm model options."""

        model = models.GPUBaseboardTemplate


class GPUBaseboardTemplateForm(FSUTemplateModelForm):
    """Form for updating a GPUBaseboardTemplate instance."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        label="FSU Type",
    )

    class Meta(FSUTemplateModelForm.Meta):
        """GPUBaseboardTemplateForm model options."""

        model = models.GPUBaseboardTemplate


class HBATemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing HBATemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.HBATemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.HBAType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """HBATemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class HBATemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of HBATemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.HBAType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="HBA type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """HBATemplateCSVForm model options."""

        model = models.HBATemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class HBATemplateCreateForm(FSUTemplatePCIModelCreateForm):
    """Form for creating one or more HBATemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all(), label="FSU Type")

    class Meta(FSUTemplatePCIModelCreateForm.Meta):
        """HBATemplateCreateForm model options."""

        model = models.HBATemplate


class HBATemplateForm(FSUTemplateModelForm):
    """Form for updating a HBATemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """HBATemplateForm model options."""

        model = models.HBATemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class MainboardTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing MainboardTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.MainboardTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """MainboardTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class MainboardTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of MainboardTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="Mainboard type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """MainboardTemplateCSVForm model options."""

        model = models.MainboardTemplate


class MainboardTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more MainboardTemplate instances."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        label="FSU Type",
    )

    class Meta(FSUTemplateCreateForm.Meta):
        """MainboardTemplateCreateForm model options."""

        model = models.MainboardTemplate


class MainboardTemplateForm(FSUTemplateModelForm):
    """Form for updating a MainboardTemplate instance."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        label="FSU Type",
    )

    class Meta(FSUTemplateModelForm.Meta):
        """MainboardTemplateForm model options."""

        model = models.MainboardTemplate


class NICTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing NICTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.NICTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.NICType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """NICTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class NICTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of NICTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.NICType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="NIC type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """NICTemplateCSVForm model options."""

        model = models.NICTemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class NICTemplateCreateForm(FSUTemplatePCIModelCreateForm):
    """Form for creating one or more NICTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all(), label="FSU Type")

    class Meta(FSUTemplatePCIModelCreateForm.Meta):
        """NICTemplateCreateForm model options."""

        model = models.NICTemplate


class NICTemplateForm(FSUTemplateModelForm):
    """Form for updating a NICTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """NICTemplateForm model options."""

        model = models.NICTemplate
        fields = ["fsu_type", "device_type", "name", "pci_slot_id", "description"]


class OtherFSUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing OtherFSUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.OtherFSUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.OtherFSUType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """OtherFSUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class OtherFSUTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of OtherFSUTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.OtherFSUType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="OtherFSU type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """OtherFSUcTemplateCSVForm model options."""

        model = models.OtherFSUTemplate


class OtherFSUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more OtherFSUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateCreateForm.Meta):
        """OtherFSUTemplateCreateForm model options."""

        model = models.OtherFSUTemplate


class OtherFSUTemplateForm(FSUTemplateModelForm):
    """Form for updating a OtherFSUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """OtherFSUTemplateForm model options."""

        model = models.OtherFSUTemplate


class PSUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing PSUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PSUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.PSUType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """PSUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]
        fields = ["fsu_type", "device_type", "name", "redundant", "description"]


class PSUTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of PSUTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.PSUType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="PSU type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """PSUTemplateCSVForm model options."""

        model = models.PSUTemplate
        fields = ["fsu_type", "device_type", "name", "redundant", "description"]


class PSUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more PSUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateCreateForm.Meta):
        """PSUTemplateCreateForm model options."""

        model = models.PSUTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "redundant", "description"]


class PSUTemplateForm(FSUTemplateModelForm):
    """Form for updating a PSUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all(), label="FSU Type")

    class Meta(FSUTemplateModelForm.Meta):
        """PSUTemplateForm model options."""

        model = models.PSUTemplate
        fields = ["fsu_type", "device_type", "name", "redundant", "description"]


class RAMModuleTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing RAMModuleTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.RAMModuleTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        required=False,
        label="FSU Type",
    )

    class Meta:
        """RAMModuleTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class RAMModuleTemplateCSVForm(FSUTemplateCSVForm):
    """Form for CSV import of RAMModuleTemplate instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        to_field_name="id",
        required=True,
        label="FSU Type",
        help_text="RAMModule type ID (name is not guaranteed to be unique)",
    )

    class Meta(FSUTemplateCSVForm.Meta):
        """RAMModuleTemplateCSVForm model options."""

        model = models.RAMModuleTemplate


class RAMModuleTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more RAMModuleTemplate instances."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        label="FSU Type",
    )
    slot_id_pattern = ExpandableNameField(label="Slot ID", required=False)
    field_order = ["device_type", "fsu_type", "name_pattern", "slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """RAMModuleTemplateCreateForm model options."""

        model = models.RAMModuleTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "slot_id_pattern", "description"]


class RAMModuleTemplateForm(FSUTemplateModelForm):
    """Form for updating a RAMModuleTemplate instance."""

    fsu_type = DynamicModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        label="FSU Type",
    )

    class Meta(FSUTemplateModelForm.Meta):
        """RAMModuleTemplateForm model options."""

        model = models.RAMModuleTemplate
        fields = ["fsu_type", "device_type", "name", "slot_id", "description"]
