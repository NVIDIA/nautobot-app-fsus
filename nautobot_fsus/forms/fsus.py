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

"""Form definitions for FSU models."""
from django import forms
from nautobot.dcim.models import Interface, PowerPort
from nautobot.utilities.forms import DynamicModelChoiceField, DynamicModelMultipleChoiceField
from nautobot.utilities.forms.constants import BOOLEAN_WITH_BLANK_CHOICES
from nautobot.utilities.forms.fields import CSVModelChoiceField, TagFilterField
from nautobot.utilities.forms.widgets import StaticSelect2

from nautobot_fsus import models
from nautobot_fsus.forms.mixins import (
    BaseFSUCSVForm,
    FSUModelBulkEditForm,
    FSUModelFilterForm,
    FSUModelForm,
    FSUImportModelForm,
)

# pylint: disable=too-many-lines


class CPUBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of CPU instances."""
    model = models.CPU

    pk = forms.ModelMultipleChoiceField(
        queryset=models.CPU.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """CPUBulkEditForm model options."""


class CPUCSVForm(BaseFSUCSVForm):
    """Form for CSV import of CPU instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.CPUType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="CPU type ID (name is not guaranteed to be unique)",
    )

    parent_mainboard = CSVModelChoiceField(
        queryset=models.Mainboard.objects.all(),
        to_field_name="id",
        required=False,
        help_text="Parent Mainboard ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """CPUCSVForm model options."""

        model = models.CPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_mainboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class CPUFilterForm(FSUModelFilterForm):
    """Form for filtering CPU instances."""

    model = models.CPU

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.CPUType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="CPU Type"
    )

    parent_mainboard = DynamicModelMultipleChoiceField(
        queryset=models.Mainboard.objects.all(),
        to_field_name="name",
        query_params={"device": "$device"},
        label="Parent Mainboard",
    )

    has_parent_mainboard = forms.NullBooleanField(
        required=False,
        label="Has Parent Mainboard",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class CPUForm(FSUModelForm):
    """Form for creating or updating CPU instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.CPUType.objects.all())

    parent_mainboard = DynamicModelChoiceField(
        queryset=models.Mainboard.objects.all(),
        query_params={"device_id": "$device"},
        required=False,
    )

    class Meta(FSUModelForm.Meta):
        """CPUForm model options."""

        model = models.CPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_mainboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class CPUImportForm(FSUImportModelForm):
    """Form for importing CPU instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.CPUType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """CPUImportForm model options."""

        model = models.CPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_mainboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class DiskBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of Disk instances."""
    model = models.Disk

    pk = forms.ModelMultipleChoiceField(
        queryset=models.Disk.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """DiskBulkEditForm model options."""


class DiskCSVForm(BaseFSUCSVForm):
    """Form for CSV import of Disk instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.DiskType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="Disk type ID (name is not guaranteed to be unique)",
    )

    parent_hba = CSVModelChoiceField(
        queryset=models.HBA.objects.all(),
        to_field_name="id",
        required=False,
        help_text="Parent HBA ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """DiskCSVForm model options."""

        model = models.Disk
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_hba",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class DiskFilterForm(FSUModelFilterForm):
    """Form for filtering Disk instances."""

    model = models.Disk

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.DiskType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="Disk Type"
    )

    parent_hba = DynamicModelMultipleChoiceField(
        queryset=models.HBA.objects.all(),
        to_field_name="name",
        query_params={"device": "$device"},
        label="Parent HBA",
    )

    tag = TagFilterField(model)


class DiskForm(FSUModelForm):
    """Form for creating or updating Disk instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.DiskType.objects.all())

    parent_hba = DynamicModelChoiceField(
        queryset=models.HBA.objects.all(),
        query_params={"device_id": "$device"},
        required=False,
    )

    class Meta(FSUModelForm.Meta):
        """DiskForm model options."""

        model = models.Disk
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_hba",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class DiskImportForm(FSUImportModelForm):
    """Form for importing Disk instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.DiskType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """DiskImportForm model options."""

        model = models.Disk
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "parent_hba",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class FanBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of Fan instances."""
    model = models.Fan

    pk = forms.ModelMultipleChoiceField(
        queryset=models.Fan.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """FanBulkEditForm model options."""


class FanCSVForm(BaseFSUCSVForm):
    """Form for CSV import of Fan instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.FanType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="Fan type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """FanCSVForm model options."""

        model = models.Fan


class FanFilterForm(FSUModelFilterForm):
    """Form for filtering Fan instances."""

    model = models.Fan

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.FanType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="Fan Type"
    )

    tag = TagFilterField(model)


class FanForm(FSUModelForm):
    """Form for creating or updating Fan instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.FanType.objects.all())

    class Meta(FSUModelForm.Meta):
        """FanForm model options."""

        model = models.Fan


class FanImportForm(FSUImportModelForm):
    """Form for importing Fan instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.FanType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """FanImportForm model options."""

        model = models.Fan


class GPUBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of GPU instances."""
    model = models.GPU

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPU.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """GPUBulkEditForm model options."""


class GPUCSVForm(BaseFSUCSVForm):
    """Form for CSV import of GPU instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.GPUType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="GPU type ID (name is not guaranteed to be unique)",
    )

    parent_gpubaseboard = CSVModelChoiceField(
        queryset=models.GPUBaseboard.objects.all(),
        to_field_name="id",
        required=False,
        help_text="Parent GPU Baseboard ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """GPUCSVForm model options."""

        model = models.GPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "parent_gpubaseboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUFilterForm(FSUModelFilterForm):
    """Form for filtering GPU instances."""

    model = models.GPU

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.GPUType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="GPU Type"
    )

    parent_gpubaseboard = DynamicModelMultipleChoiceField(
        queryset=models.GPUBaseboard.objects.all(),
        to_field_name="name",
        query_params={"device": "$device"},
        label="Parent GPU Baseboard",
    )

    tag = TagFilterField(model)


class GPUForm(FSUModelForm):
    """Form for creating or updating GPU instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUType.objects.all())

    parent_gpubaseboard = DynamicModelChoiceField(
        queryset=models.GPUBaseboard.objects.all(),
        query_params={"device_id": "$device"},
        required=False,
    )

    has_parent_gpubaseboard = forms.NullBooleanField(
        required=False,
        label="Has Parent GPU Baseboard",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    class Meta(FSUModelForm.Meta):
        """GPUForm model options."""

        model = models.GPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "parent_gpubaseboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUImportForm(FSUImportModelForm):
    """Form for importing GPU instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.GPUType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """GPUImportForm model options."""

        model = models.GPU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "parent_gpubaseboard",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUBaseboardBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of GPUBaseboard instances."""
    model = models.GPUBaseboard

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GPUBaseboard.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        required=False,
    )

    class Meta(FSUModelBulkEditForm.Meta):
        """GPUBaseboardBulkEditForm model options."""


class GPUBaseboardCSVForm(BaseFSUCSVForm):
    """Form for CSV import of GPUBaseboard instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="GPUBaseboard type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """GPUBaseboardCSVForm model options."""

        model = models.GPUBaseboard


class GPUBaseboardFilterForm(FSUModelFilterForm):
    """Form for filtering GPUBaseboard instances."""

    model = models.GPUBaseboard

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="GPUBaseboard Type"
    )

    has_child_gpus = forms.NullBooleanField(
        required=False,
        label="Has Child GPU(s)",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class GPUBaseboardForm(FSUModelForm):
    """Form for creating or updating GPUBaseboard instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.GPUBaseboardType.objects.all())

    gpus = DynamicModelMultipleChoiceField(
        queryset=models.GPU.objects.all(),
        query_params={"device_id": "$device", "has_parent_gpubaseboard": "false"},
        required=False,
        label="GPUS",
    )

    class Meta(FSUModelForm.Meta):
        """GPUBaseboardForm model options."""

        model = models.GPUBaseboard
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "gpus",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUBaseboardImportForm(FSUImportModelForm):
    """Form for importing GPUBaseboard instances."""

    fsu_type = forms.ModelChoiceField(
        queryset=models.GPUBaseboardType.objects.all(),
        to_field_name="name",
    )

    class Meta(FSUImportModelForm.Meta):
        """GPUBaseboardImportForm model options."""

        model = models.GPUBaseboard


class HBABulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of HBA instances."""
    model = models.HBA

    pk = forms.ModelMultipleChoiceField(
        queryset=models.HBA.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """HBABulkEditForm model options."""


class HBACSVForm(BaseFSUCSVForm):
    """Form for CSV import of HBA instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.HBAType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="HBA type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """HBACSVForm model options."""

        model = models.HBA
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class HBAFilterForm(FSUModelFilterForm):
    """Form for filtering HBA instances."""

    model = models.HBA

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.HBAType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="HBA Type"
    )

    has_child_disks = forms.NullBooleanField(
        required=False,
        label="Has Child Disk(s)",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class HBAForm(FSUModelForm):
    """Form for creating or updating HBA instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.HBAType.objects.all())

    disks = DynamicModelMultipleChoiceField(
        queryset=models.Disk.objects.all(),
        query_params={"device_id": "$device", "has_parent_hba": "false"},
        required=False,
        label="Disks",
    )

    class Meta(FSUModelForm.Meta):
        """HBAForm model options."""

        model = models.HBA
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "disks",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class HBAImportForm(FSUImportModelForm):
    """Form for importing HBA instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.HBAType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """HBAImportForm model options."""

        model = models.HBA
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class MainboardBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of Mainboard instances."""
    model = models.Mainboard

    pk = forms.ModelMultipleChoiceField(
        queryset=models.Mainboard.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.MainboardType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """MainboardBulkEditForm model options."""


class MainboardCSVForm(BaseFSUCSVForm):
    """Form for CSV import of Mainboard instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="Mainboard type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """MainboardCSVForm model options."""

        model = models.Mainboard


class MainboardFilterForm(FSUModelFilterForm):
    """Form for filtering Mainboard instances."""

    model = models.Mainboard

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="Mainboard Type"
    )

    has_child_cpus = forms.NullBooleanField(
        required=False,
        label="Has Child CPU(s)",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class MainboardForm(FSUModelForm):
    """Form for creating or updating Mainboard instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.MainboardType.objects.all())

    cpus = DynamicModelMultipleChoiceField(
        queryset=models.CPU.objects.all(),
        query_params={"device_id": "$device", "has_parent_mainboard": "false"},
        required=False,
        label="CPUs",
    )

    class Meta(FSUModelForm.Meta):
        """MainboardForm model options."""

        model = models.Mainboard
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "cpus",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class MainboardImportForm(FSUImportModelForm):
    """Form for importing Mainboard instances."""

    fsu_type = forms.ModelChoiceField(
        queryset=models.MainboardType.objects.all(),
        to_field_name="name",
    )

    class Meta(FSUImportModelForm.Meta):
        """MainboardImportForm model options."""

        model = models.Mainboard


class NICBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of NIC instances."""
    model = models.NIC

    pk = forms.ModelMultipleChoiceField(
        queryset=models.NIC.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """NICBulkEditForm model options."""


class NICCSVForm(BaseFSUCSVForm):
    """Form for CSV import of NIC instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.NICType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="NIC type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """NICCSVForm model options."""

        model = models.NIC
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class NICFilterForm(FSUModelFilterForm):
    """Form for filtering NIC instances."""

    model = models.NIC

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.NICType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="NIC Type"
    )

    has_child_interfaces = forms.NullBooleanField(
        required=False,
        label="Has Child Interfaces(s)",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class NICForm(FSUModelForm):
    """Form for creating or updating NIC instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.NICType.objects.all())

    interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        query_params={
            "device_id": "$device",
            "type__n": ["bridge", "lag", "virtual"],
            "nautobot_fsus_has_parent_nic": "false",
        },
        required=False,
        label="Interfaces",
    )

    class Meta(FSUModelForm.Meta):
        """NICForm model options."""

        model = models.NIC
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "interfaces",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class NICImportForm(FSUImportModelForm):
    """Form for importing NIC instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.NICType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """NICImportForm model options."""

        model = models.NIC
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class OtherFSUBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of OtherFSU instances."""
    model = models.OtherFSU

    pk = forms.ModelMultipleChoiceField(
        queryset=models.OtherFSU.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """OtherFSUBulkEditForm model options."""


class OtherFSUCSVForm(BaseFSUCSVForm):
    """Form for CSV import of OtherFSU instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.OtherFSUType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="OtherFSU type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """OtherFSUCSVForm model options."""

        model = models.OtherFSU


class OtherFSUFilterForm(FSUModelFilterForm):
    """Form for filtering OtherFSU instances."""

    model = models.OtherFSU

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.OtherFSUType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="OtherFSU Type"
    )

    tag = TagFilterField(model)


class OtherFSUForm(FSUModelForm):
    """Form for creating or updating OtherFSU instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.OtherFSUType.objects.all())

    class Meta(FSUModelForm.Meta):
        """OtherFSUForm model options."""

        model = models.OtherFSU


class OtherFSUImportForm(FSUImportModelForm):
    """Form for importing OtherFSU instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.OtherFSUType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """OtherFSUImportForm model options."""

        model = models.OtherFSU


class PSUBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of PSU instances."""
    model = models.PSU

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PSU.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """PSUBulkEditForm model options."""


class PSUCSVForm(BaseFSUCSVForm):
    """Form for CSV import of PSU instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.PSUType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="PSU type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """PSUCSVForm model options."""

        model = models.PSU


class PSUFilterForm(FSUModelFilterForm):
    """Form for filtering PSU instances."""

    model = models.PSU

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.PSUType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="PSU Type"
    )

    has_child_power_ports = forms.NullBooleanField(
        required=False,
        label="Has Child Power Ports(s)",
        widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    tag = TagFilterField(model)


class PSUForm(FSUModelForm):
    """Form for creating or updating PSU instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.PSUType.objects.all())

    power_ports = DynamicModelMultipleChoiceField(
        queryset=PowerPort.objects.all(),
        query_params={"device_id": "$device", "nautobot_fsus_has_parent_psu": "false"},
        required=False,
        label="Power Ports",
    )

    class Meta(FSUModelForm.Meta):
        """PSUForm model options."""

        model = models.PSU
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "power_ports",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class PSUImportForm(FSUImportModelForm):
    """Form for importing PSU instances."""

    fsu_type = forms.ModelChoiceField(
        queryset=models.PSUType.objects.all(),
        to_field_name="name",
    )

    class Meta(FSUImportModelForm.Meta):
        """PSUImportForm model options."""

        model = models.PSU


class RAMModuleBulkEditForm(FSUModelBulkEditForm):
    """Form for bulk editing of RAMModule instances."""
    model = models.RAMModule

    pk = forms.ModelMultipleChoiceField(
        queryset=models.RAMModule.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )

    fsu_type = DynamicModelChoiceField(queryset=models.RAMModuleType.objects.all(), required=False)

    class Meta(FSUModelBulkEditForm.Meta):
        """RAMModuleBulkEditForm model options."""


class RAMModuleCSVForm(BaseFSUCSVForm):
    """Form for CSV import of RAMModule instances."""

    fsu_type = CSVModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        to_field_name="id",
        required=True,
        help_text="RAMModule type ID (name is not guaranteed to be unique)",
    )

    class Meta(BaseFSUCSVForm.Meta):
        """RAMModuleCSVForm model options."""

        model = models.RAMModule
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class RAMModuleFilterForm(FSUModelFilterForm):
    """Form for filtering RAMModule instances."""

    model = models.RAMModule

    fsu_type_id = DynamicModelChoiceField(
        queryset=models.RAMModuleType.objects.all(),
        query_params={"manufacturer": "$manufacturer"},
        required=False,
        label="RAMModule Type"
    )

    tag = TagFilterField(model)


class RAMModuleForm(FSUModelForm):
    """Form for creating or updating RAMModule instances."""

    fsu_type = DynamicModelChoiceField(queryset=models.RAMModuleType.objects.all())

    class Meta(FSUModelForm.Meta):
        """RAMModuleForm model options."""

        model = models.RAMModule
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class RAMModuleImportForm(FSUImportModelForm):
    """Form for importing RAMModule instances."""

    fsu_type = forms.ModelChoiceField(queryset=models.RAMModuleType.objects.all(), to_field_name="name")

    class Meta(FSUImportModelForm.Meta):
        """RAMModuleImportForm model options."""

        model = models.RAMModule
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]
