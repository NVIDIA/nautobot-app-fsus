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

"""Template extensions for built-in Nautobot models."""
from typing import Any, Type
from uuid import UUID

from django.urls import reverse
from nautobot.apps.ui import TemplateExtension
from nautobot.users.models import User

from nautobot_fsus import models, tables
from nautobot_fsus.models.mixins import FSUTemplateModel
from nautobot_fsus.tables.mixins import FSUTemplateModelTable

# pylint: disable=abstract-method


class FSUsTabContentTemplate(TemplateExtension):
    """Extend the template for a Nautobot model."""

    model: str
    obj_pk: UUID
    fsu_count: int
    parent_type: str

    def buttons(self) -> str:
        """Add button with menu for adding FSUs."""
        user: User | None = getattr(self.context["request"], "user", None)

        buttons: list[str] = []

        if user is not None and user.has_perm(f"dcim.change_{self.parent_type}"):
            return_url = reverse(
                f"plugins:nautobot_fsus:{self.parent_type}_fsus_tab",
                kwargs={"pk": self.obj_pk},
            )

            buttons.extend([
                "<div class=\"btn-group\">",
                "    <button type=\"button\" class=\"btn btn-primary dropdown-toggle\" "
                "data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">",
                "        <span class=\"mdi mdi-plus-thick\" aria-hidden=\"true\"></span> "
                "Add FSUs <span class=\"caret\"></span>",
                "    </button>",
                "    <ul class=\"dropdown-menu\">",
            ])

            if user.has_perm("nautobot_fsus.add_cpu"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:cpu_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"CPUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_disk"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:disk_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"Disks</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_fan"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:fan_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"Fans</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_gpu"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:gpu_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"GPUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_gpubaseboard"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:gpubaseboard_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"GPU Baseboards</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_hba"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:hba_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"HBAs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_mainboard"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:mainboard_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"Mainboards</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_nic"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:nic_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"NICs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_otherfsu"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:otherfsu_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"Other FSUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_psu"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:psu_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"PSUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_rammodule"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:rammodule_add')}"
                    f"?{self.parent_type}={self.obj_pk}"
                    f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                    f"RAM Modules</a></li>"
                )

            buttons.extend(["    </ul>", "</div>"])

        return "\n".join(buttons)

    def detail_tabs(self) -> list[dict[str, Any]]:
        """Add a tab for displaying child FSUs."""
        tabs: list[dict[str, Any]] = []

        if self.fsu_count > 0:
            tabs.append(
                {
                    "title": self.render(
                        "nautobot_fsus/inc/tab_title.html",
                        extra_context={"title": "FSUs", "item_count": self.fsu_count},
                    ),
                    "url": reverse(
                        f"plugins:nautobot_fsus:{self.parent_type}_fsus_tab",
                        kwargs={"pk": self.obj_pk},
                    ),
                },
            )

        return tabs


class DeviceFSUsTabContent(FSUsTabContentTemplate):
    """Extend the template for a Device."""

    model = "dcim.device"

    def __init__(self, context: dict[str, Any]) -> None:
        """Calculate child FSU counts."""
        super().__init__(context)

        self.obj_pk = self.context["object"].pk
        self.parent_type = "device"

        fsus = {
            "cpus": models.CPU.objects.filter(device__pk=self.obj_pk).count(),
            "disks": models.Disk.objects.filter(device__pk=self.obj_pk).count(),
            "fans": models.Fan.objects.filter(device__pk=self.obj_pk).count(),
            "gpus": models.GPU.objects.filter(device__pk=self.obj_pk).count(),
            "gpubaseboards": models.GPUBaseboard.objects.filter(device__pk=self.obj_pk).count(),
            "hbas": models.HBA.objects.filter(device__pk=self.obj_pk).count(),
            "mainboards": models.Mainboard.objects.filter(device__pk=self.obj_pk).count(),
            "nics": models.NIC.objects.filter(device__pk=self.obj_pk).count(),
            "otherfsus": models.OtherFSU.objects.filter(device__pk=self.obj_pk).count(),
            "psus": models.PSU.objects.filter(device__pk=self.obj_pk).count(),
            "rammodules": models.RAMModule.objects.filter(device__pk=self.obj_pk).count(),
        }
        self.fsu_count = sum(fsus.values())
        self.context["fsus"] = fsus
        self.context["parent_type"] = self.parent_type


class DeviceTypeFSUsContent(TemplateExtension):
    """Extend the template for a Device Type."""

    model = "dcim.devicetype"

    def __init__(self, context: dict[str, Any]) -> None:
        """Set base properties."""
        super().__init__(context)

        self.obj_pk = self.context["object"].pk
        self.fsu_count = 0
        self.parent_type = "devicetype"

    def buttons(self) -> str:
        """Add button with menu for adding FSUs."""
        user: User | None = getattr(self.context["request"], "user", None)

        buttons: list[str] = []

        if user is not None and user.has_perm("dcim.change_devicetype"):
            buttons.extend([
                "<div class=\"btn-group\">",
                "    <button type=\"button\" class=\"btn btn-primary dropdown-toggle\" "
                "data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">",
                "        <span class=\"mdi mdi-plus-thick\" aria-hidden=\"true\"></span> "
                "Add FSUs <span class=\"caret\"></span>",
                "    </button>",
                "    <ul class=\"dropdown-menu\">",
            ])

            if user.has_perm("nautobot_fsus.add_cputemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:cputemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_cpus\">"
                    f"CPUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_disktemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:disktemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_disks\">"
                    f"Disks</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_fantemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:fantemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_fans\">"
                    f"Fans</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_gputemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:gputemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_gpus\">"
                    f"GPUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_gpubaseboardtemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:gpubaseboardtemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_gpubaseboards\">"
                    f"GPU Baseboards</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_hbatemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:hbatemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_hbas\">"
                    f"HBAs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_mainboardtemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:mainboardtemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_mainboards\">"
                    f"Mainboards</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_nictemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:nictemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_nics\">"
                    f"NICs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_otherfsutemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:otherfsutemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_otherfsus\">"
                    f"Other FSUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_psutemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:psutemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_psus\">"
                    f"PSUs</a></li>"
                )
            if user.has_perm("nautobot_fsus.add_rammoduletemplate"):
                buttons.append(
                    f"        <li><a href=\"{reverse('plugins:nautobot_fsus:rammoduletemplate_add')}"
                    f"?device_type={self.obj_pk}"
                    f"&return_url={self.context['object'].get_absolute_url()}%23tab_rammodules\">"
                    f"RAM Modules</a></li>"
                )

            buttons.extend(["    </ul>", "</div>"])

        return "\n".join(buttons)

    def full_width_page(self) -> str:
        """Add tables for FSU templates."""
        def _fsu_table(
            table: Type[FSUTemplateModelTable],
            fsu: Type[FSUTemplateModel],
        ) -> FSUTemplateModelTable:
            """Helper method to setup the table for an FSU template."""
            fsu_table: FSUTemplateModelTable = table(
                fsu.objects.filter(device_type__pk=self.obj_pk)
            )
            fsu_table.columns.hide("device_type")
            return fsu_table

        user: User | None = getattr(self.context["request"], "user", None)

        self.context["cpu_table"] = _fsu_table(tables.CPUTemplateTable, models.CPUTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_cputemplate"):
            self.context["cpu_table"].columns.show("pk")

        self.context["disk_table"] = _fsu_table(tables.DiskTemplateTable, models.DiskTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_disktemplate"):
            self.context["disk_table"].columns.show("pk")

        self.context["fan_table"] = _fsu_table(tables.FanTemplateTable, models.FanTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_fantemplate"):
            self.context["fan_table"].columns.show("pk")

        self.context["gpu_table"] = _fsu_table(tables.GPUTemplateTable, models.GPUTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_gputemplate"):
            self.context["gpu_table"].columns.show("pk")

        self.context["gpubaseboard_table"] = _fsu_table(
            tables.GPUBaseboardTemplateTable,
            models.GPUBaseboardTemplate,
        )
        if user is not None and user.has_perm("nautobot_fsus.change_gpubaseboardtemplate"):
            self.context["gpubaseboard_table"].columns.show("pk")

        self.context["hba_table"] = _fsu_table(tables.HBATemplateTable, models.HBATemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_hbatemplate"):
            self.context["hba_table"].columns.show("pk")

        self.context["mainboard_table"] = _fsu_table(
            tables.MainboardTemplateTable,
            models.MainboardTemplate,
        )
        if user is not None and user.has_perm("nautobot_fsus.change_mainboardtemplate"):
            self.context["mainboard_table"].columns.show("pk")

        self.context["nic_table"] = _fsu_table(tables.NICTemplateTable, models.NICTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_nictemplate"):
            self.context["nic_table"].columns.show("pk")

        self.context["otherfsu_table"] = _fsu_table(
            tables.OtherFSUTemplateTable,
            models.OtherFSUTemplate,
        )
        if user is not None and user.has_perm("nautobot_fsus.change_otherfsutemplate"):
            self.context["otherfsu_table"].columns.show("pk")

        self.context["psu_table"] = _fsu_table(tables.PSUTemplateTable, models.PSUTemplate)
        if user is not None and user.has_perm("nautobot_fsus.change_psutemplate"):
            self.context["psu_table"].columns.show("pk")

        self.context["rammodule_table"] = _fsu_table(
            tables.RAMModuleTemplateTable,
            models.RAMModuleTemplate,
        )
        if user is not None and user.has_perm("nautobot_fsus.change_rammoduletemplate"):
            self.context["rammodule_table"].columns.show("pk")

        rendered: str = self.render("nautobot_fsus/inc/devicetype_fsus.html")
        return rendered


class InterfaceParentNICContent(TemplateExtension):
    """Extend the template for an Inteface."""

    model = "dcim.Interface"

    def right_page(self) -> str:
        """Add a panel for the parent NIC."""
        if self.context["object"].type in ("bridge", "lag", "virtual"):
            return ""

        rendered: str = self.render("nautobot_fsus/inc/parent_nic_panel.html")
        return rendered


class LocationFSUTabContent(FSUsTabContentTemplate):
    """Extend the template for a Location."""

    model = "dcim.location"

    def __init__(self, context: dict[str, Any]) -> None:
        """Calculate child FSU counts."""
        super().__init__(context)

        self.obj_pk = self.context["object"].pk
        self.parent_type = "location"

        fsus = {
            "cpus": models.CPU.objects.filter(location__pk=self.obj_pk).count(),
            "disks": models.Disk.objects.filter(location__pk=self.obj_pk).count(),
            "fans": models.Fan.objects.filter(location__pk=self.obj_pk).count(),
            "gpus": models.GPU.objects.filter(location__pk=self.obj_pk).count(),
            "gpubaseboards": models.GPUBaseboard.objects.filter(location__pk=self.obj_pk).count(),
            "hbas": models.HBA.objects.filter(location__pk=self.obj_pk).count(),
            "mainboards": models.Mainboard.objects.filter(location__pk=self.obj_pk).count(),
            "nics": models.NIC.objects.filter(location__pk=self.obj_pk).count(),
            "otherfsus": models.OtherFSU.objects.filter(location__pk=self.obj_pk).count(),
            "psus": models.PSU.objects.filter(location__pk=self.obj_pk).count(),
            "rammodules": models.RAMModule.objects.filter(location__pk=self.obj_pk).count(),
        }
        self.fsu_count = sum(fsus.values())
        self.context["fsus"] = fsus
        self.context["parent_type"] = self.parent_type


class PowerPortParentPSUContent(TemplateExtension):
    """Extend the template for a Power Port."""

    model = "dcim.PowerPort"

    def right_page(self) -> str:
        """Add a panel for the parent PSU."""
        rendered: str = self.render("nautobot_fsus/inc/parent_psu_panel.html")
        return rendered


template_extensions = [
    DeviceFSUsTabContent,
    DeviceTypeFSUsContent,
    InterfaceParentNICContent,
    LocationFSUTabContent,
    PowerPortParentPSUContent,
]
