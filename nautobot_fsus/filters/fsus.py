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

"""FilterSets for FSU models."""
import django_filters
from nautobot.extras.filters import NautobotFilterSet
from nautobot.extras.filters.mixins import StatusModelFilterSetMixin
from nautobot.utilities.filters import (
    NaturalKeyOrPKMultipleChoiceFilter,
    RelatedMembershipBooleanFilter,
)

from nautobot_fsus import models
from nautobot_fsus.filters.mixins import FSUModelFilterSetMixin


class CPUFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for CPUs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.CPUType.objects.all(),
        label="CPU Type (ID)",
    )

    parent_mainboard = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="parent_mainboard",
        queryset=models.Mainboard.objects.all(),
        to_field_name="name",
        label="Parent Mainboard (Name or ID)",
    )

    has_parent_mainboard = RelatedMembershipBooleanFilter(
        field_name="parent_mainboard",
        label="Has a parent Mainboard",
    )

    class Meta:
        """CPUFilterSet model options."""

        model = models.CPU
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class DiskFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for Disks."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.DiskType.objects.all(),
        label="Disk Type (ID)",
    )

    parent_hba = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="parent_hba",
        queryset=models.HBA.objects.all(),
        to_field_name="name",
        label="Parent HBA (Name or ID)",
    )

    has_parent_hba = RelatedMembershipBooleanFilter(
        field_name="parent_hba",
        label="Has a parent HBA",
    )

    class Meta:
        """DiskFilterSet model options."""

        model = models.Disk
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class FanFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for Fans."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.FanType.objects.all(),
        label="Fan Type (ID)",
    )

    class Meta:
        """FanFilterSet model options."""

        model = models.Fan
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUBaseboardFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for GPU Baseboards."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.GPUBaseboardType.objects.all(),
        label="GPU Baseboard Type (ID)",
    )

    has_child_gpus = RelatedMembershipBooleanFilter(
        field_name="gpus",
        label="Has Child GPUs",
    )

    class Meta:
        """GPUBaseboardFilterSet model options."""

        model = models.GPUBaseboard
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class GPUFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for GPUs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.GPUType.objects.all(),
        label="GPU Type (ID)",
    )

    has_parent_gpubaseboard = RelatedMembershipBooleanFilter(
        field_name="parent_gpubaseboard",
        label="Has a parent GPU Baseboard",
    )

    parent_gpubaseboard = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="parent_gpubaseboard",
        queryset=models.GPUBaseboard.objects.all(),
        to_field_name="name",
        label="Parent GPU Baseboard (Name or ID)",
    )

    class Meta:
        """GPUFilterSet model options."""

        model = models.GPU
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class HBAFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for HBAs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.HBAType.objects.all(),
        label="HBA Type (ID)",
    )

    has_child_disks = RelatedMembershipBooleanFilter(
        field_name="disks",
        label="Has Child Disks",
    )

    class Meta:
        """HBAFilterSet model options."""

        model = models.HBA
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class MainboardFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for Mainboards."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.MainboardType.objects.all(),
        label="Mainboard Type (ID)",
    )

    has_child_cpus = RelatedMembershipBooleanFilter(
        field_name="cpus",
        label="Has Child CPUs",
    )

    class Meta:
        """MainboardFilterSet model options."""

        model = models.Mainboard
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class NICFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for NICs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.NICType.objects.all(),
        label="NIC Type (ID)",
    )

    has_child_interfaces = RelatedMembershipBooleanFilter(
        field_name="interfaces",
        label="Has Child Interfaces",
    )

    class Meta:
        """NICFilterSet model options."""

        model = models.NIC
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class OtherFSUFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for Other FSUs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.OtherFSUType.objects.all(),
        label="Other FSU Type (ID)",
    )

    class Meta:
        """OtherFSUFilterSet model options."""

        model = models.OtherFSU
        fields = [
            "id",
            "name",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class PSUFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for PSUs."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.PSUType.objects.all(),
        label="PSU Type (ID)",
    )

    has_child_power_ports = RelatedMembershipBooleanFilter(
        field_name="power_ports",
        label="Has Child Power Ports",
    )

    class Meta:
        """PSUFilterSet model options."""

        model = models.PSU
        fields = [
            "id",
            "name",
            "serial_number",
            "redundant",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]


class RAMModuleFilterSet(
    NautobotFilterSet,
    FSUModelFilterSetMixin,
    StatusModelFilterSetMixin,
):
    """Filter set for RAM Modules."""

    fsu_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=models.RAMModuleType.objects.all(),
        label="RAM Module Type (ID)",
    )

    class Meta:
        """RAMModuleFilterSet model options."""

        model = models.RAMModule
        fields = [
            "id",
            "name",
            "slot_id",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
            "comments",
        ]
