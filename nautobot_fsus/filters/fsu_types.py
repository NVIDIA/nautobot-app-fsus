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

"""FilterSets for FSU type models."""
import django_filters.constants
from nautobot.extras.filters import NautobotFilterSet

from nautobot_fsus import models
from nautobot_fsus.choices import (
    CPUArchitectures,
    DiskTypes,
    MemoryModuleTypes,
    MemoryTechnologies,
    PCIeGenerations,
    PSUFeedType,
)
from nautobot_fsus.filters.mixins import FSUTypeModelFilterSetMixin


class CPUTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for CPU types."""

    architecture = django_filters.MultipleChoiceFilter(
        choices=CPUArchitectures,
        label="CPU Architecture",
    )

    pcie_generation = django_filters.MultipleChoiceFilter(
        choices=PCIeGenerations,
        label="PCIe Generation",
    )

    class Meta:
        """CPUTypeFilterSet model options."""

        model = models.CPUType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "comments",
            "instances",
        ]


class DiskTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for disk types."""

    disk_type = django_filters.MultipleChoiceFilter(
        choices=DiskTypes,
        label="Disk Type",
    )

    class Meta:
        """DiskTypeFilterSet model options."""

        model = models.DiskType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "disk_type",
            "size",
            "description",
            "comments",
            "instances",
        ]


class FanTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for fan types."""

    class Meta:
        """FanTypeFilterSet model options."""

        model = models.FanType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
            "instances",
        ]


class GPUBaseboardTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for GPU base board types."""

    gpu_count__isnull = django_filters.BooleanFilter(
        field_name="slot_count",
        lookup_expr="isnull",
        distinct=False,
        exclude=False,
    )

    class Meta:
        """GPUBaseboardTypeFilterSet model options."""

        model = models.GPUBaseboardType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "slot_count",
            "description",
            "comments",
            "instances",
        ]


class GPUTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for GPU types."""

    class Meta:
        """GPUTypeFilterSet model options."""

        model = models.GPUType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
            "instances",
        ]


class HBATypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for HBA types."""

    class Meta:
        """HBATypeFilterSet model options."""

        model = models.HBAType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
            "instances",
        ]


class MainboardTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for Mainboard types."""

    class Meta:
        """MainboardTypeFilterSet model options."""

        model = models.MainboardType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "cpu_socket_count",
            "description",
            "comments",
            "instances",
        ]


class NICTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for NIC types."""

    interface_count__isnull = django_filters.BooleanFilter(
        field_name="interface_count",
        lookup_expr="isnull",
        distinct=False,
        exclude=False,
    )

    class Meta:
        """NICTypeFilterSet model options."""

        model = models.NICType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "interface_count",
            "description",
            "comments",
            "instances",
        ]


class OtherFSUTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for Other FSU types."""

    class Meta:
        """OtherFSUTypeFilterSet model options."""

        model = models.OtherFSUType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "description",
            "comments",
            "instances",
        ]


class PSUTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for PSU types."""

    feed_type = django_filters.MultipleChoiceFilter(
        choices=PSUFeedType,
        label="Power Feed Type",
    )

    class Meta:
        """PSUTypeFilterSet model options."""

        model = models.PSUType
        fields = [
            "id",
            "manufacturer",
            "name",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "comments",
            "instances",
        ]


class RAMModuleTypeFilterSet(NautobotFilterSet, FSUTypeModelFilterSetMixin):
    """Filter set for RAM module types."""

    module_type = django_filters.MultipleChoiceFilter(
        choices=MemoryModuleTypes,
    )

    technology = django_filters.MultipleChoiceFilter(
        choices=MemoryTechnologies,
    )

    class Meta:
        """RAMModuleTypeFilterSet model options."""

        model = models.RAMModuleType
        fields = [
            "id",
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
            "instances",
        ]
