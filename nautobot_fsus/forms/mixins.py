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
from nautobot.apps.forms import (
    BootstrapMixin,
    CommentField,
    DynamicModelChoiceField,
    ExpandableNameField,
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    StatusModelBulkEditFormMixin,
    StatusModelFilterFormMixin,
    TagsBulkEditFormMixin,
)
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer

from nautobot_fsus.models.mixins import FSUModel


class FSUTemplateModelForm(NautobotModelForm):
    """Abstract form model for creating/editing FSU templates."""

    device_type = DynamicModelChoiceField(queryset=DeviceType.objects.all(), label="Device Type")

    class Meta:
        """FSUTemplateModelForm model options."""

        abstract = True
        fields = ["fsu_type", "device_type", "name", "description"]
        widgets = {"device_type": forms.HiddenInput()}


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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the form and add query params as needed."""
        super().__init__(*args, **kwargs)

        if self.instance.device is not None:
            location_tree = list(self.instance.device.location.ancestors(include_self=True))

            # If there is more than one location in the tree, assume the top-level ancestor
            # is a Region, and filter one level down from it.
            self.fields["location"].widget.add_query_param(
                "subtree",
                location_tree[1].name if len(location_tree) > 1 else location_tree[0].name,
            )

            # If parent is a device, the FSU can't have a status of Available.
            self.fields["status"].widget.add_query_param("name__n", "Available")
        elif self.instance.location is not None:
            location_tree = list(self.instance.location.ancestors(include_self=True))

            # If there is more than one location in the tree, assume the top-level ancestor
            # is a Region, and filter one level down from it.
            self.fields["device"].widget.add_query_param(
                "location",
                location_tree[1].name if len(location_tree) > 1 else location_tree[0].name,
            )

            # If parent is a location, the FSU can't have a status of Active.
            self.fields["status"].widget.add_query_param("name__n", "Active")


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
        queryset=Device.objects.all(), to_field_name="name", required=False
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
