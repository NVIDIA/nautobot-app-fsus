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

"""Form mixins and base classes to handle user-definable fields for FSU and FSUTypes models."""
from typing import Any, Type

from django import forms
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer
from nautobot.extras.forms import (
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    TagsBulkEditFormMixin,
    StatusModelBulkEditFormMixin,
    StatusModelFilterFormMixin,
)
from nautobot.extras.forms.mixins import StatusModelCSVFormMixin
from nautobot.utilities.forms import BootstrapMixin, CommentField, CSVModelForm
from nautobot.utilities.forms.fields import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
    ExpandableNameField,
)

from nautobot_fsus.models.mixins import FSUModel


class FSUTemplateModelForm(NautobotModelForm):
    """Abstract form model for creating/editing FSU templates."""

    device_type = DynamicModelChoiceField(queryset=DeviceType.objects.all(), label="Device Type")

    class Meta:
        """FSUTemplateModelForm model options."""

        abstract = True
        fields = ["fsu_type", "device_type", "name", "description"]
        widgets = {"device_type": forms.HiddenInput()}


class FSUTemplateCSVForm(CSVModelForm):
    """Abstract form model for bulk importing FSU templates from CSV data."""

    device_type = CSVModelChoiceField(queryset=DeviceType.objects.all(), label="Device Type")

    class Meta:
        """FSUTemplateCSVForm model options."""

        abstract = True
        fields = ["fsu_type", "device_type", "name", "description"]


class FSUTemplateCreateForm(BootstrapMixin, forms.Form):
    """Base form for creating FSU templates."""

    name_pattern = ExpandableNameField(label="Name")
    device_type = DynamicModelChoiceField(queryset=DeviceType.objects.all(), label="Device Type")
    description = forms.CharField(required=False)

    field_order = ["device_type", "fsu_type", "name_pattern", "description"]

    class Meta:
        """FSUTemplateCreateForm model options."""

        abstract = True
        fields = ["fsu_type", "device_type", "name_pattern", "description"]
        widgets = {"device_type": forms.HiddenInput()}

    def clean(self):
        """Validate the form data."""
        super().clean()

        # Validate that the number of generated names and pci_slot_ids are equal
        name_count = len(self.cleaned_data["name_pattern"])
        if "pci_slot_id_pattern" in self.cleaned_data and self.cleaned_data["pci_slot_id_pattern"]:
            pci_slot_count = len(self.cleaned_data["pci_slot_id_pattern"])
            if name_count != pci_slot_count:
                raise forms.ValidationError(
                    message={
                        "pci_slot_id_pattern": forms.ValidationError(
                            message="The provided name pattern will create %(names)d names, "
                                    "however, %(pci_slots)d pci_slot_ids will be generated - "
                                    "these counts must match.",
                            params={"names": name_count, "pci_slot_ids": pci_slot_count},
                        ),
                    },
                    code="pattern_mismatch",
                )
        elif "slot_id_pattern" in self.cleaned_data and self.cleaned_data["slot_id_pattern"]:
            slot_count = len(self.cleaned_data["slot_id_pattern"])
            if name_count != slot_count:
                raise forms.ValidationError(
                    message={
                        "slot_id_pattern": forms.ValidationError(
                            message="The provided name pattern will create %(names)d names, "
                                    "however, %(slots)d slot_ids will be generated - "
                                    "these counts must match.",
                            params={"names": name_count, "slot_ids": slot_count},
                        ),
                    },
                    code="pattern_mismatch",
                )


class FSUTemplatePCIModelCreateForm(FSUTemplateCreateForm):
    """Abstract for extension to handle pci_slot_id field."""

    pci_slot_id_pattern = ExpandableNameField(label="PCI Slot ID", required=False)
    field_order = ["device_type", "fsu_type", "name_pattern", "pci_slot_id_pattern", "description"]

    class Meta(FSUTemplateCreateForm.Meta):
        """FSUTemplatePCIModelCreateForm model options."""

        abstract = True
        fields = ["device_type", "fsu_type", "name_pattern", "pci_slot_id_pattern", "description"]


class FSUTypeModelForm(NautobotModelForm):
    """Abstract form model for creating/editing FSU types."""

    manufacturer = DynamicModelChoiceField(queryset=Manufacturer.objects.all())
    comments = CommentField(label="Comments")

    class Meta:
        """Metaclass attributes."""
        abstract = True
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
            "tags",
        ]


class FSUTypeCSVForm(CSVModelForm):
    """Abstract form model for bulk importing FSU types from CSV data."""

    manufacturer = CSVModelChoiceField(queryset=Manufacturer.objects.all(), to_field_name="name")

    class Meta:
        """FSUTypeCSVForm model options."""

        abstract = True
        fields = ["manufacturer", "name", "part_number", "description", "comments"]


class FSUTypeImportModelForm(BootstrapMixin, forms.ModelForm):
    """Abstract form model for importing FSU types."""

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
    )

    class Meta:
        """Metaclass attributes."""
        abstract = True
        fields = [
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
        ]


class FSUModelForm(NautobotModelForm):
    """Abstract form model for creating/editing FSUs."""

    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False)
    comments = CommentField(label="Comments", required=False)

    class Meta:
        """Metaclass attributes."""
        abstract = True
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class FSUModelBulkEditForm(
    NautobotBulkEditForm,
    TagsBulkEditFormMixin,
    StatusModelBulkEditFormMixin,
):
    """Abstract form model for bulk editing FSUs."""

    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False)
    firmware_version = forms.CharField(max_length=32, required=False)
    driver_version = forms.CharField(max_length=32, required=False)
    driver_name = forms.CharField(max_length=100, required=False)

    class Meta:
        """FSUModelBulkEditForm model options."""

        abstract = True
        nullable_fields: list[str] = [
            "device",
            "location",
            "firmware_version",
            "driver_version",
            "driver_name",
        ]


class FSUModelFilterForm(NautobotFilterForm, StatusModelFilterFormMixin):
    """Form for filtering CPU instances."""
    model: Type[FSUModel]

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        required=False,
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=False,
    )

    q = forms.CharField(required=False, label="Search")


class FSUImportModelForm(BootstrapMixin, forms.ModelForm):
    """Abstract form model for importing FSUs."""
    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        required=False
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=False,
    )

    class Meta:
        """Metaclass attributes."""
        abstract = True
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class BaseFSUCSVForm(StatusModelCSVFormMixin):
    """Base form for CSV exports of FSUs."""
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        required=False,
        blank=True,
        help_text="Parent device (must be empty if storage location is set)."
    )

    location = CSVModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=False,
        blank=True,
        help_text="Parent storage location (must be empty if device is set)."
    )

    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=False,
        help_text="FSU type manufacturer"
    )

    class Meta:
        """Metadata attributes."""
        abstract = True
        fields = [
            "device",
            "location",
            "name",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]

    def __init__(self, *args: Any, data: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """Initialize the form."""
        if "headers" not in kwargs:
            headers = {
                "device": "name",
                "location": "name",
                "name": None,
                "fsu_type": "id",
                "status": "slug",
            }
        else:
            headers = kwargs.pop("headers")
            headers.setdefault("device", "name")
            headers.setdefault("location", "name")

        super().__init__(*args, headers=headers, **kwargs)

        if data is not None:
            if manufacturer_name := data.get("manufacturer"):
                params = {
                    f"manufacturer__{self.fields['manufacturer'].to_field_name}": manufacturer_name
                }
                self.fields["fsu_type"].queryset = self.fields["fsu_type"].queryset.filter(**params)
