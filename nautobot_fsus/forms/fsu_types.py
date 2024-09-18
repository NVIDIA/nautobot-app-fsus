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

"""Form definitions for FSU type models."""
from django import forms
from nautobot.dcim.models import Manufacturer
from nautobot.extras.forms import NautobotBulkEditForm, NautobotFilterForm, TagsBulkEditFormMixin
from nautobot.utilities.forms.fields import DynamicModelChoiceField, TagFilterField

from nautobot_fsus import choices, models
from nautobot_fsus.forms.mixins import (
    FSUTypeModelForm,
    FSUTypeCSVForm,
    FSUTypeImportModelForm,
)


class CPUTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing CPUType instances."""

    model = models.CPUType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.CPUType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    cpu_speed = forms.FloatField(min_value=0.1, required=False)
    cores = forms.IntegerField(min_value=1, required=False)

    architecture = forms.ChoiceField(
        choices=choices.CPUArchitectures,
        initial=choices.CPUArchitectures.x86,
        label="CPU Architecture",
    )

    pcie_generation = forms.ChoiceField(
        choices=choices.PCIeGenerations,
        initial=choices.PCIeGenerations.gen6,
        required=False,
    )

    class Meta:
        """CPUTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["pcie_generation"]


class CPUTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk import of CPUType instances."""

    class Meta:
        """CPUTypeCSVForm model options."""

        model = models.CPUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "comments",
        ]


class CPUTypeFilterForm(NautobotFilterForm):
    """Form for filtering CPUType instances."""

    model = models.CPUType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class CPUTypeForm(FSUTypeModelForm):
    """Form for creating or updating CPUType instances."""

    architecture = forms.ChoiceField(choices=choices.CPUArchitectures, label="CPU Architecture")

    pcie_generation = forms.TypedChoiceField(
        choices=choices.PCIeGenerations,
        required=False,
        label="PCIe Generation",
        empty_value=None,
    )

    class Meta(FSUTypeModelForm.Meta):
        """CPUTypeForm model options."""

        model = models.CPUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "comments",
            "tags",
        ]


class CPUTypeImportForm(FSUTypeImportModelForm):
    """Form for importing CPUType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """CPUTypeImportForm model options."""

        model = models.CPUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "comments",
            "tags",
        ]


class DiskTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing DiskType instances."""

    model = models.DiskType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.DiskType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    size = forms.IntegerField(min_value=1, required=False)

    disk_type = forms.ChoiceField(
        choices=choices.DiskTypes,
        initial=choices.DiskTypes.disk_ssd,
        required=False,
    )

    class Meta:
        """DiskTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["size"]


class DiskTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk import of DiskType instances."""

    class Meta:
        """DiskTypeCSVForm model options."""

        model = models.DiskType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "disk_type",
            "size",
            "description",
            "comments",
        ]


class DiskTypeFilterForm(NautobotFilterForm):
    """Form for filtering DiskType instances."""

    model = models.DiskType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class DiskTypeForm(FSUTypeModelForm):
    """Form for creating or updating DiskType instances."""

    disk_type = forms.ChoiceField(choices=choices.DiskTypes)

    class Meta(FSUTypeModelForm.Meta):
        """DiskTypeForm model options."""

        model = models.DiskType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "disk_type",
            "size",
            "description",
            "comments",
            "tags",
        ]


class DiskTypeImportForm(FSUTypeImportModelForm):
    """Form for importing DiskType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """DiskTypeImportForm model options."""

        model = models.DiskType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "disk_type",
            "size",
            "description",
            "comments",
            "tags",
        ]


class FanTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing FanType instances."""

    model = models.FanType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.FanType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        """FanTypeBulkEditForm model options."""

        nullable_fields: list[str] = []


class FanTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk import of FanType instances."""

    class Meta(FSUTypeCSVForm.Meta):
        """FanTypeCSVForm model options."""

        model = models.FanType


class FanTypeFilterForm(NautobotFilterForm):
    """Form for filtering FanType instances."""

    model = models.FanType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class FanTypeForm(FSUTypeModelForm):
    """Form for creating or updating FanType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """FanTypeForm model options."""

        model = models.FanType


class FanTypeImportForm(FSUTypeImportModelForm):
    """Form for importing FanType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """FanTypeImportForm model options."""

        model = models.FanType


class GPUTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing GPUType instances."""

    model = models.GPUType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        """GPUTypeBulkEditForm model options."""

        nullable_fields: list[str] = []


class GPUTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk editing GPUType instances."""

    class Meta(FSUTypeCSVForm.Meta):
        """GPUTypeBulkEditForm model options."""

        model = models.GPUType


class GPUTypeFilterForm(NautobotFilterForm):
    """Form for filtering GPUType instances."""

    model = models.GPUType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class GPUTypeForm(FSUTypeModelForm):
    """Form for creating or updating GPUType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """GPUTypeForm model options."""

        model = models.GPUType


class GPUTypeImportForm(FSUTypeImportModelForm):
    """Form for importing GPUType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """GPUTypeImportForm model options."""

        model = models.GPUType


class GPUBaseboardTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing GPUBaseboardType instances."""

    model = models.GPUBaseboardType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    slot_count = forms.IntegerField(min_value=1, required=False)

    class Meta:
        """GPUBaseboardTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["slot_count"]


class GPUBaseboardTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk editing GPUBaseboardType instances."""

    class Meta:
        """GPUBaseboardTypeCSVForm model options."""

        model = models.GPUBaseboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "slot_count",
            "description",
            "comments",
        ]


class GPUBaseboardTypeFilterForm(NautobotFilterForm):
    """Form for filtering GPUBaseboardType instances."""

    model = models.GPUBaseboardType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class GPUBaseboardTypeForm(FSUTypeModelForm):
    """Form for creating or updating GPUBaseboardType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """GPUBaseboardTypeForm model options."""

        model = models.GPUBaseboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "slot_count",
            "description",
            "comments",
            "tags",
        ]


class GPUBaseboardTypeImportForm(FSUTypeImportModelForm):
    """Form for importing GPUBaseboardType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """GPUBaseboardTypeImportForm model options."""

        model = models.GPUBaseboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "slot_count",
            "description",
            "comments",
            "tags",
        ]


class HBATypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing HBAType instances."""

    model = models.HBAType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.HBAType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        """HBATypeBulkEditForm model options."""

        nullable_fields: list[str] = []


class HBATypeCSVForm(FSUTypeCSVForm):
    """Form for bulk editing HBAType instances."""

    class Meta(FSUTypeCSVForm.Meta):
        """HBATypeCSVForm model options."""

        model = models.HBAType


class HBATypeFilterForm(NautobotFilterForm):
    """Form for filtering HBAType instances."""

    model = models.HBAType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class HBATypeForm(FSUTypeModelForm):
    """Form for creating or updating HBAType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """HBATypeForm model options."""

        model = models.HBAType


class HBATypeImportForm(FSUTypeImportModelForm):
    """Form for importing HBAType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """HBATypeImportForm model options."""

        model = models.HBAType


class MainboardTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing MainboardType instances."""

    model = models.MainboardType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.MainboardType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    cpu_socket_count = forms.IntegerField(min_value=1, required=False)

    class Meta:
        """MainboardTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["cpu_socket_count"]


class MainboardTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk importing MainboardType instances."""

    class Meta:
        """MainboardTypeCSVForm model options."""

        model = models.MainboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "cpu_socket_count",
            "description",
            "comments",
        ]


class MainboardTypeFilterForm(NautobotFilterForm):
    """Form for filtering MainboardType instances."""

    model = models.MainboardType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class MainboardTypeForm(FSUTypeModelForm):
    """Form for creating or updating MainboardType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """MainboardTypeForm model options."""

        model = models.MainboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "cpu_socket_count",
            "description",
            "comments",
            "tags",
        ]


class MainboardTypeImportForm(FSUTypeImportModelForm):
    """Form for importing MainboardType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """MainboardTypeImportForm model options."""

        model = models.MainboardType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "cpu_socket_count",
            "description",
            "comments",
            "tags",
        ]


class NICTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing NICType instances."""

    model = models.NICType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.NICType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    interface_count = forms.IntegerField(min_value=1, required=False)

    class Meta:
        """NICTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["interface_count"]


class NICTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk importing NICType instances."""

    class Meta:
        """NICTypeCSVForm model options."""

        model = models.NICType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "interface_count",
            "description",
            "comments",
        ]


class NICTypeFilterForm(NautobotFilterForm):
    """Form for filtering NICType instances."""

    model = models.NICType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class NICTypeForm(FSUTypeModelForm):
    """Form for creating or updating NICType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """NICTypeForm model options."""

        model = models.NICType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "interface_count",
            "description",
            "comments",
            "tags",
        ]


class NICTypeImportForm(FSUTypeImportModelForm):
    """Form for importing NICType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """NICTypeImportForm model options."""

        model = models.NICType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "interface_count",
            "description",
            "comments",
            "tags",
        ]


class OtherFSUTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing OtherFSUType instances."""

    model = models.OtherFSUType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.OtherFSUType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)

    class Meta:
        """OtherFSUTypeBulkEditForm model options."""

        nullable_fields: list[str] = []


class OtherFSUTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk importing OtherFSUType instances."""

    class Meta(FSUTypeCSVForm.Meta):
        """OtherFSUTypeCSVForm model options."""

        model = models.OtherFSUType


class OtherFSUTypeFilterForm(NautobotFilterForm):
    """Form for filtering OtherFSUType instances."""

    model = models.OtherFSUType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class OtherFSUTypeForm(FSUTypeModelForm):
    """Form for creating or updating OtherFSUType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """OtherFSUTypeForm model options."""

        model = models.OtherFSUType


class OtherFSUTypeImportForm(FSUTypeImportModelForm):
    """Form for importing OtherFSUType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """OtherFSUTypeImportForm model options."""

        model = models.OtherFSUType


class PSUTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing PSUType instances."""

    model = models.PSUType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PSUType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    power_provided = forms.IntegerField(min_value=1, required=False)
    required_voltage = forms.CharField(max_length=32, required=False)
    hot_swappable = forms.BooleanField(required=False)

    feed_type = forms.ChoiceField(
        choices=choices.PSUFeedType,
        initial=choices.PSUFeedType.psu_dc,
        required=False,
    )

    class Meta:
        """PSUTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["power_provided", "required_voltage"]


class PSUTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk importing PSUType instances."""

    class Meta:
        """PSUTypeCSVForm model options."""

        model = models.PSUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "comments",
        ]


class PSUTypeFilterForm(NautobotFilterForm):
    """Form for filtering PSUType instances."""

    model = models.PSUType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class PSUTypeForm(FSUTypeModelForm):
    """Form for creating or updating PSUType instances."""

    feed_type = forms.ChoiceField(
        choices=choices.PSUFeedType,
        initial=choices.PSUFeedType.psu_dc,
        required=False,
    )

    class Meta(FSUTypeModelForm.Meta):
        """PSUTypeForm model options."""

        model = models.PSUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "comments",
            "tags",
        ]


class PSUTypeImportForm(FSUTypeImportModelForm):
    """Form for importing PSUType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """PSUTypeImportForm model options."""

        model = models.PSUType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "comments",
            "tags",
        ]


class RAMModuleTypeBulkEditForm(NautobotBulkEditForm, TagsBulkEditFormMixin):
    """Form for bulk editing RAMModuleType instances."""

    model = models.RAMModuleType

    pk = forms.ModelMultipleChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        widget=forms.MultipleHiddenInput,
    )

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all(), required=False)
    speed = forms.IntegerField(min_value=1, required=False)
    capacity = forms.IntegerField(min_value=1, required=False)
    quantity = forms.IntegerField(min_value=1, required=False)

    module_type = forms.ChoiceField(
        choices=choices.MemoryModuleTypes,
        initial=choices.MemoryModuleTypes.udimm,
        required=False,
    )

    technology = forms.ChoiceField(
        choices=choices.MemoryTechnologies,
        initial=choices.MemoryTechnologies.ddr5,
        required=False,
    )

    class Meta:
        """RAMModuleTypeBulkEditForm model options."""

        nullable_fields: list[str] = ["speed", "capacity", "quantity"]


class RAMModuleTypeCSVForm(FSUTypeCSVForm):
    """Form for bulk importing RAMModuleType instances."""

    class Meta:
        """RAMModuleTypeCSVForm model options."""

        model = models.RAMModuleType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "module_type",
            "technology",
            "speed",
            "capacity",
            "quantity",
            "description",
            "comments",
        ]


class RAMModuleTypeFilterForm(NautobotFilterForm):
    """Form for filtering RAMModuleType instances."""

    model = models.RAMModuleType

    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
    )

    tags = TagFilterField(model)
    q = forms.CharField(required=False, label="Search")


class RAMModuleTypeForm(FSUTypeModelForm):
    """Form for creating or updating RAMModuleType instances."""

    class Meta(FSUTypeModelForm.Meta):
        """RAMModuleTypeForm model options."""

        model = models.RAMModuleType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "module_type",
            "technology",
            "speed",
            "capacity",
            "quantity",
            "description",
            "comments",
            "tags",
        ]


class RAMModuleTypeImportForm(FSUTypeImportModelForm):
    """Form for importing RAMModuleType instances."""

    class Meta(FSUTypeImportModelForm.Meta):
        """RAMModuleTypeImportForm model options."""

        model = models.RAMModuleType
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "module_type",
            "technology",
            "speed",
            "capacity",
            "quantity",
            "description",
            "comments",
            "tags",
        ]
