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

"""FilterSets for FSU template models."""
import django_filters.constants
from nautobot.extras.filters.mixins import CustomFieldModelFilterSetMixin
from nautobot.utilities.filters import BaseFilterSet, MultiValueCharFilter

from nautobot_fsus import models
from nautobot_fsus.filters.mixins import FSUTemplateModelFilterSetMixin


class CPUTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for CPUTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.CPUType.objects.all(),
        label="CPU Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.CPUType.objects.all(),
        to_field_name="name",
        label="CPU Type (name)",
    )

    class Meta:
        """CPUTemplateFilterSet model options."""

        model = models.CPUTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class DiskTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for DiskTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.DiskType.objects.all(),
        label="Disk Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.DiskType.objects.all(),
        to_field_name="name",
        label="Disk Type (name)",
    )

    class Meta:
        """DiskTemplateFilterSet model options."""

        model = models.DiskTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class FanTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for FanTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.FanType.objects.all(),
        label="Fan Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.FanType.objects.all(),
        to_field_name="name",
        label="Fan Type (name)",
    )

    class Meta:
        """FanTemplateFilterSet model options."""

        model = models.FanTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class GPUBaseboardTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for GPUBaseboardTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.GPUBaseboardType.objects.all(),
        label="GPU Baseboard Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.GPUBaseboardType.objects.all(),
        to_field_name="name",
        label="GPU Baseboard Type (name)",
    )

    class Meta:
        """GPUBaseboardTemplateFilterSet model options."""

        model = models.GPUBaseboardTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class GPUTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for GPUTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.GPUType.objects.all(),
        label="GPU Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.GPUType.objects.all(),
        to_field_name="name",
        label="GPU Type (name)",
    )

    pci_slot_id = MultiValueCharFilter(label="PCI Slot ID")

    class Meta:
        """GPUTemplateFilterSet model options."""

        model = models.GPUTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "pci_slot_id",
            "description",
        ]


class HBATemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for HBATemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.HBAType.objects.all(),
        label="HBA Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.HBAType.objects.all(),
        to_field_name="name",
        label="HBA Type (name)",
    )

    class Meta:
        """HBATemplateFilterSet model options."""

        model = models.HBATemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "pci_slot_id",
            "description",
        ]


class MainboardTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for MainboardTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.MainboardType.objects.all(),
        label="Mainboard Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.MainboardType.objects.all(),
        to_field_name="name",
        label="Mainboard Type (name)",
    )

    class Meta:
        """MainboardTemplateFilterSet model options."""

        model = models.MainboardTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class NICTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for NICTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.NICType.objects.all(),
        label="NIC Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.NICType.objects.all(),
        to_field_name="name",
        label="NIC Type (name)",
    )

    pci_slot_id = MultiValueCharFilter(label="PCI Slot ID")

    class Meta:
        """NICTemplateFilterSet model options."""

        model = models.NICTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "pci_slot_id",
            "description",
        ]


class OtherFSUTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for OtherFSTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.OtherFSUType.objects.all(),
        label="Other FSU Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.OtherFSUType.objects.all(),
        to_field_name="name",
        label="Other FSU Type (name)",
    )

    class Meta:
        """OtherFSUTemplateFilterSet model options."""

        model = models.OtherFSUTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "description",
        ]


class PSUTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for PSUTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.PSUType.objects.all(),
        label="PSU Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.PSUType.objects.all(),
        to_field_name="name",
        label="PSU Type (name)",
    )

    class Meta:
        """PSUTemplateFilterSet model options."""

        model = models.PSUTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "redundant",
            "description",
        ]


class RAMModuleTemplateFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSetMixin,
    FSUTemplateModelFilterSetMixin,
):
    """Filter set for RAMModuleTemplate."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.RAMModuleType.objects.all(),
        label="RAM Module Type (ID)",
    )

    fsu_type = django_filters.ModelMultipleChoiceFilter(
        field_name="fsu_type__name",
        queryset=models.RAMModuleType.objects.all(),
        to_field_name="name",
        label="RAM Module Type (name)",
    )

    slot_id = MultiValueCharFilter(label="Slot ID")

    class Meta:
        """RAMModuleTemplateFilterSet model options."""

        model = models.RAMModuleTemplate
        fields = [
            "id",
            "device_type",
            "fsu_type",
            "name",
            "slot_id",
            "description",
        ]
