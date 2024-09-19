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
from nautobot.utilities.forms.fields import DynamicModelChoiceField, ExpandableNameField

from nautobot_fsus import models
from nautobot_fsus.forms.mixins import FSUTemplateCreateForm, FSUTemplateModelForm


class CPUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing CPUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.CPUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all(), required=False)

    class Meta:
        """CPUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class CPUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more CPUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """CPUTemplateCreateForm model options."""

        model = models.CPUTemplate


class CPUTemplateForm(FSUTemplateModelForm):
    """Form for updating a CPUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """CPUTemplateForm model options."""

        model = models.CPUTemplate


class DiskTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing DiskTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.DiskTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all(), required=False)

    class Meta:
        """DiskTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class DiskTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more DiskTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """DiskTemplateCreateForm model options."""

        model = models.DiskTemplate


class DiskTemplateForm(FSUTemplateModelForm):
    """Form for updating a DiskTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """DiskTemplateForm model options."""

        model = models.DiskTemplate


class FanTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing FanTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.FanTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all(), required=False)

    class Meta:
        """FanTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class FanTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more FanTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """FanTemplateCreateForm model options."""

        model = models.FanTemplate


class FanTemplateForm(FSUTemplateModelForm):
    """Form for updating a FanTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """FanTemplateForm model options."""

        model = models.FanTemplate


class GPUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing GPUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all(), required=False)

    class Meta:
        """GPUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class GPUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more GPUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all())
    pci_slot_id_pattern = ExpandableNameField(label="PCI Slot ID")
    field_order = ["device_type", "fsu_type", "name_pattern", "pci_slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """GPUTemplateCreateForm model options."""

        model = models.GPUTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "pci_slot_id_pattern", "description"]


class GPUTemplateForm(FSUTemplateModelForm):
    """Form for updating a GPUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all())

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
    )

    class Meta:
        """GPUBaseboardTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class GPUBaseboardTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more GPUBaseboardTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUBaseboardType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """GPUBaseboardTemplateCreateForm model options."""

        model = models.GPUBaseboardTemplate


class GPUBaseboardTemplateForm(FSUTemplateModelForm):
    """Form for updating a GPUBaseboardTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUBaseboardType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """GPUBaseboardTemplateForm model options."""

        model = models.GPUBaseboardTemplate


class HBATemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing HBATemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.HBATemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all(), required=False)

    class Meta:
        """HBATemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class HBATemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more HBATemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all())
    pci_slot_id_pattern = ExpandableNameField(label="PCI Slot ID")
    field_order = ["device_type", "fsu_type", "name_pattern", "pci_slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """HBATemplateCreateForm model options."""

        model = models.HBATemplate
        fields = ["fsu_type", "device_type", "name_pattern", "pci_slot_id_pattern", "description"]


class HBATemplateForm(FSUTemplateModelForm):
    """Form for updating a HBATemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all())

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
    )

    class Meta:
        """MainboardTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class MainboardTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more MainboardTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.MainboardType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """MainboardTemplateCreateForm model options."""

        model = models.MainboardTemplate


class MainboardTemplateForm(FSUTemplateModelForm):
    """Form for updating a MainboardTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.MainboardType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """MainboardTemplateForm model options."""

        model = models.MainboardTemplate


class NICTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing NICTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.NICTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all(), required=False)

    class Meta:
        """NICTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class NICTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more NICTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all())
    pci_slot_id_pattern = ExpandableNameField(label="PCI Slot ID")
    field_order = ["device_type", "fsu_type", "name_pattern", "pci_slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """NICTemplateCreateForm model options."""

        model = models.NICTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "pci_slot_id_pattern", "description"]


class NICTemplateForm(FSUTemplateModelForm):
    """Form for updating a NICTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all())

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

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all(), required=False)

    class Meta:
        """OtherFSUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class OtherFSUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more OtherFSUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """OtherFSUTemplateCreateForm model options."""

        model = models.OtherFSUTemplate


class OtherFSUTemplateForm(FSUTemplateModelForm):
    """Form for updating a OtherFSUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """OtherFSUTemplateForm model options."""

        model = models.OtherFSUTemplate


class PSUTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk editing PSUTemplate instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PSUTemplate.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all(), required=False)

    class Meta:
        """PSUTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class PSUTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more PSUTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all())

    class Meta(FSUTemplateCreateForm.Meta):
        """PSUTemplateCreateForm model options."""

        model = models.PSUTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "redundant", "description"]


class PSUTemplateForm(FSUTemplateModelForm):
    """Form for updating a PSUTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all())

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

    fsu_type = DynamicModelChoiceField(queryset=models.RAMModuleType.objects.all(), required=False)

    class Meta:
        """RAMModuleTemplateBulkEditForm model options."""

        nullable_fields = ["description"]


class RAMModuleTemplateCreateForm(FSUTemplateCreateForm):
    """Form for creating one or more RAMModuleTemplate instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.RAMModuleType.objects.all())
    slot_id_pattern = ExpandableNameField(label="Slot ID")
    field_order = ["device_type", "fsu_type", "name_pattern", "slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """RAMModuleTemplateCreateForm model options."""

        model = models.RAMModuleTemplate
        fields = ["fsu_type", "device_type", "name_pattern", "slot_id_pattern", "description"]


class RAMModuleTemplateForm(FSUTemplateModelForm):
    """Form for updating a RAMModuleTemplate instance."""

    fsu_type = DynamicModelChoiceField(queryset=models.RAMModuleType.objects.all())

    class Meta(FSUTemplateModelForm.Meta):
        """RAMModuleTemplateForm model options."""

        model = models.RAMModuleTemplate
        fields = ["fsu_type", "device_type", "name", "slot_id", "description"]
