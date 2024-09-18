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

"""Table definitions for FSUType models."""
from nautobot.utilities.tables import ButtonsColumn, LinkedCountColumn, TagColumn

from nautobot_fsus import models
from nautobot_fsus.tables.mixins import FSUTypeModelTable


class CPUTypeTable(FSUTypeModelTable):
    """Table for displaying CPUType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:cputype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:cpu_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.CPUType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """CPUTypeTable model options."""

        model = models.CPUType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
            "instance_count",
            "actions",
        ]


class DiskTypeTable(FSUTypeModelTable):
    """Table for displaying DiskType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:disktype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:disk_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.DiskType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """DiskTypeTable model options."""

        model = models.DiskType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "disk_type",
            "size",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "disk_type",
            "size",
            "description",
            "instance_count",
            "actions",
        ]


class FanTypeTable(FSUTypeModelTable):
    """Table for displaying FanType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:fantype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:fan_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.FanType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """FanTypeTable model options."""

        model = models.FanType


class GPUTypeTable(FSUTypeModelTable):
    """Table for displaying GPUType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:gputype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:gpu_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.GPUType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUTypeTable model options."""

        model = models.GPUType


class GPUBaseboardTypeTable(FSUTypeModelTable):
    """Table for displaying GPUBaseboardType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:gpubaseboardtype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:gpubaseboard_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.GPUBaseboardType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUBaseboardTypeTable model options."""

        model = models.GPUBaseboardType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "slot_count",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "slot_count",
            "description",
            "instance_count",
            "actions",
        ]


class HBATypeTable(FSUTypeModelTable):
    """Table for displaying HBAType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:hbatype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:hba_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.HBAType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """HBATypeTable model options."""

        model = models.HBAType


class MainboardTypeTable(FSUTypeModelTable):
    """Table for displaying MainboardType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:mainboardtype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:mainboard_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.MainboardType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """MainboardTypeTable model options."""

        model = models.MainboardType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "cpu_socket_count",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "cpu_socket_count",
            "description",
            "instance_count",
            "actions",
        ]


class NICTypeTable(FSUTypeModelTable):
    """Table for displaying NICType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:nictype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:nic_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.NICType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """NICTypeTable model options."""

        model = models.NICType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "interface_count",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "interface_count",
            "description",
            "instance_count",
            "actions",
        ]


class OtherFSUTypeTable(FSUTypeModelTable):
    """Table for displaying OtherFSUType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:otherfsutype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:otherfsu_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.OtherFSUType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """OtherFSUTypeTable model options."""

        model = models.OtherFSUType


class PSUTypeTable(FSUTypeModelTable):
    """Table for displaying PSUType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:psutype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:psu_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.PSUType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """PSUTypeTable model options."""

        model = models.PSUType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
            "instance_count",
            "actions",
        ]


class RAMModuleTypeTable(FSUTypeModelTable):
    """Table for displaying RAMModuleType instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:rammoduletype_list")

    instance_count = LinkedCountColumn(
        viewname="plugins:nautobot_fsus:rammodule_list",
        url_params={"fsu_type_id": "pk"},
        verbose_name="Instances",
    )

    actions = ButtonsColumn(models.RAMModuleType, buttons=("edit", "delete"))

    class Meta(FSUTypeModelTable.Meta):  # pylint: disable=too-few-public-methods
        """RAMModuleTypeTable model options."""

        model = models.RAMModuleType
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "technology",
            "speed",
            "capacity",
            "quantity",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "technology",
            "capacity",
            "description",
            "instance_count",
            "actions",
        ]
