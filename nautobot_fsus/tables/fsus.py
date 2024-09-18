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

"""Table definitions for FSU models."""
import django_tables2 as tables
from django_tables2.utils import Accessor
from nautobot.utilities.tables import BaseTable, ButtonsColumn, TagColumn

from nautobot_fsus import models
from nautobot_fsus.tables.mixins import FSUModelTable


class CPUTable(FSUModelTable):
    """Table for displaying CPU instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:cpu_list")
    actions = ButtonsColumn(models.CPU, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:cputype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """CPUTable model options."""

        model = models.CPU


class CPUImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """CPUImportTable model options."""

        model = models.CPU
        fields = ["name", "fsu_type", "parent"]


class DiskTable(FSUModelTable):
    """Table for displaying Disk instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:disk_list")
    actions = ButtonsColumn(models.Disk, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:disktype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """DiskTable model options."""

        model = models.Disk


class DiskImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """DiskImportTable model options."""

        model = models.Disk
        fields = ["name", "fsu_type", "parent"]


class FanTable(FSUModelTable):
    """Table for displaying Fan instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:fan_list")
    actions = ButtonsColumn(models.Fan, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:fantype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """FanTable model options."""

        model = models.Fan


class FanImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """FanImportTable model options."""

        model = models.Fan
        fields = ["name", "fsu_type", "parent"]


class GPUTable(FSUModelTable):
    """Table for displaying GPU instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:gpu_list")
    actions = ButtonsColumn(models.GPU, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:gputype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUTable model options."""

        model = models.GPU
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]


class GPUImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUImportTable model options."""

        model = models.GPU
        fields = ["name", "fsu_type", "parent"]


class GPUBaseboardTable(FSUModelTable):
    """Table for displaying GPUBaseboard instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:gpubaseboard_list")
    actions = ButtonsColumn(models.GPUBaseboard, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:gpubaseboardtype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUBaseboardTable model options."""

        model = models.GPUBaseboard


class GPUBaseboardImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUBaseboardImportTable model options."""

        model = models.GPUBaseboard
        fields = ["name", "fsu_type", "parent"]


class HBATable(FSUModelTable):
    """Table for displaying HBA instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:hba_list")
    actions = ButtonsColumn(models.HBA, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:hbatype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """HBATable model options."""

        model = models.HBA
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]


class HBAImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """HBAImportTable model options."""

        model = models.HBA
        fields = ["name", "fsu_type", "parent"]


class MainboardTable(FSUModelTable):
    """Table for displaying Mainboard instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:mainboard_list")
    actions = ButtonsColumn(models.Mainboard, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:mainboardtype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """MainboardTable model options."""

        model = models.Mainboard


class MainboardImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """MainboardImportTable model options."""

        model = models.Mainboard
        fields = ["name", "fsu_type", "parent"]


class NICTable(FSUModelTable):
    """Table for displaying NIC instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:nic_list")
    actions = ButtonsColumn(models.NIC, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:nictype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """NICTable model options."""

        model = models.NIC
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "pci_slot_id",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]


class NICImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """NICImportTable model options."""

        model = models.NIC
        fields = ["name", "fsu_type", "parent"]


class OtherFSUTable(FSUModelTable):
    """Table for displaying OtherFSU instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:otherfsu_list")
    actions = ButtonsColumn(models.OtherFSU, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:otherfsutype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """OtherFSUTable model options."""

        model = models.OtherFSU


class OtherFSUImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """OtherFSUImportTable model options."""

        model = models.OtherFSU
        fields = ["name", "fsu_type", "parent"]


class PSUTable(FSUModelTable):
    """Table for displaying PSU instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:psu_list")
    actions = ButtonsColumn(models.PSU, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:psutype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """PSUTable model options."""

        model = models.PSU
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "redundant",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "redundant",
            "status",
            "actions",
        ]


class PSUImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """PSUImportTable model options."""

        model = models.PSU
        fields = ["name", "fsu_type", "parent"]


class RAMModuleTable(FSUModelTable):
    """Table for displaying RAMModule instances."""

    tags = TagColumn(url_name="plugins:nautobot_fsus:rammodule_list")
    actions = ButtonsColumn(models.RAMModule, buttons=("edit", "delete"))

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:rammoduletype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    class Meta(FSUModelTable.Meta):  # pylint: disable=too-few-public-methods
        """RAMModuleTable model options."""

        model = models.RAMModule
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "slot_id",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]


class RAMModuleImportTable(BaseTable):
    """Table for the post-bulk import view."""

    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}")

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """RAMModuleImportTable model options."""

        model = models.RAMModule
        fields = ["name", "fsu_type", "parent"]
