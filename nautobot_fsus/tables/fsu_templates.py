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

"""Table definitions for FSUTemplate models."""
import django_tables2 as tables
from django_tables2.utils import Accessor
from nautobot.utilities.tables import ButtonsColumn

from nautobot_fsus import models
from nautobot_fsus.tables.mixins import FSUTemplateModelTable


class CPUTemplateTable(FSUTemplateModelTable):
    """Table for displaying CPUTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:cputype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.CPUTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """CPUTemplateTable model options."""

        model = models.CPUTemplate


class DiskTemplateTable(FSUTemplateModelTable):
    """Table for displaying DiskTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:disktype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.DiskTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """DiskTemplateTable model options."""

        model = models.DiskTemplate


class FanTemplateTable(FSUTemplateModelTable):
    """Table for displaying FanTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:fantype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.FanTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """FanTemplateTable model options."""

        model = models.FanTemplate


class GPUTemplateTable(FSUTemplateModelTable):
    """Table for displaying GPUTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:gputype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.GPUTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUTemplateTable model options."""

        model = models.GPUTemplate
        fields = [
            "pk",
            "name",
            "fsu_type",
            "device_type",
            "pci_slot_id",
            "description",
            "actions",
        ]


class GPUBaseboardTemplateTable(FSUTemplateModelTable):
    """Table for displaying GPUBaseboardTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:gpubaseboardtype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.GPUBaseboardTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUBaseboardTemplateTable model options."""

        model = models.GPUBaseboardTemplate


class HBATemplateTable(FSUTemplateModelTable):
    """Table for displaying HBATemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:hbatype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.HBATemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """HBATemplateTable model options."""

        model = models.HBATemplate
        fields = [
            "pk",
            "name",
            "fsu_type",
            "device_type",
            "pci_slot_id",
            "description",
            "actions",
        ]


class MainboardTemplateTable(FSUTemplateModelTable):
    """Table for displaying MainboardTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:mainboardtype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.MainboardTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """MainboardTemplateTable model options."""

        model = models.MainboardTemplate


class NICTemplateTable(FSUTemplateModelTable):
    """Table for displaying GPUTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:nictype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.NICTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """GPUTemplateTable model options."""

        model = models.NICTemplate
        fields = [
            "pk",
            "name",
            "fsu_type",
            "device_type",
            "pci_slot_id",
            "description",
            "actions",
        ]


class OtherFSUTemplateTable(FSUTemplateModelTable):
    """Table for displaying OtherFSUTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:otherfsutype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.OtherFSUTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """OtherFSUTemplateTable model options."""

        model = models.OtherFSUTemplate


class PSUTemplateTable(FSUTemplateModelTable):
    """Table for displaying PSUTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:psutype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.PSUTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """PSUTemplateTable model options."""

        model = models.PSUTemplate
        fields = ["pk", "name", "fsu_type", "device_type", "redundant", "description", "actions"]


class RAMModuleTemplateTable(FSUTemplateModelTable):
    """Table for displaying RAMModuleTemplate instances."""

    fsu_type = tables.LinkColumn(
        viewname="plugins:nautobot_fsus:rammoduletype",
        args=[Accessor("fsu_type__pk")],
        verbose_name="Type",
        text=lambda record: record.fsu_type.display,
    )

    actions = ButtonsColumn(models.RAMModuleTemplate, buttons=("edit", "delete"))

    class Meta(FSUTemplateModelTable.Meta):  # pylint: disable=too-few-public-methods
        """RAMModuleTemplateTable model options."""

        model = models.RAMModuleTemplate
        fields = [
            "pk",
            "name",
            "fsu_type",
            "device_type",
            "slot_id",
            "description",
            "actions",
        ]
