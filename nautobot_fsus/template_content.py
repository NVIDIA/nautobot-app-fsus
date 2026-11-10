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

from typing import Any, ClassVar, Type
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

    fsu_models: ClassVar[list[tuple[str, str]]] = [
        ("cpu", "CPUs"),
        ("disk", "Disks"),
        ("fan", "Fans"),
        ("gpu", "GPUs"),
        ("gpubaseboard", "GPU Baseboards"),
        ("hba", "HBAs"),
        ("lpumodule", "LPU Modules"),
        ("mainboard", "Mainboards"),
        ("nic", "NICs"),
        ("otherfsu", "Other FSUs"),
        ("psu", "PSUs"),
        ("rammodule", "RAM Modules"),
    ]

    def buttons(self) -> str:
        """Add button with menu for adding FSUs."""
        user: User | None = getattr(self.context["request"], "user", None)

        buttons: list[str] = []

        if user is not None and user.has_perm(f"dcim.change_{self.parent_type}"):
            return_url = reverse(
                f"plugins:nautobot_fsus:{self.parent_type}_fsus_tab",
                kwargs={"pk": self.obj_pk},
            )

            buttons.extend(
                [
                    '<div class="btn-group">',
                    '    <button type="button" class="btn btn-primary dropdown-toggle" '
                    'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">',
                    '        <span class="mdi mdi-plus-thick" aria-hidden="true"></span> '
                    'Add FSUs <span class="caret"></span>',
                    "    </button>",
                    '    <ul class="dropdown-menu">',
                ]
            )

            for model_key, label in self.fsu_models:
                if user.has_perm(f"nautobot_fsus.add_{model_key}"):
                    buttons.append(
                        f"        <li><a href=\"{reverse(f'plugins:nautobot_fsus:{model_key}_add')}"
                        f"?{self.parent_type}={self.obj_pk}"
                        f"&return_url={return_url}%3Ftab=nautobot_fsus:1\">"
                        f"{label}</a></li>"
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
            "lpumodules": models.LPUModule.objects.filter(device__pk=self.obj_pk).count(),
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

    fsu_template_models: ClassVar[list[tuple[str, str, str]]] = [
        ("cpu", "cpus", "CPUs"),
        ("disk", "disks", "Disks"),
        ("fan", "fans", "Fans"),
        ("gpu", "gpus", "GPUs"),
        ("gpubaseboard", "gpubaseboards", "GPU Baseboards"),
        ("hba", "hbas", "HBAs"),
        ("lpumodule", "lpumodules", "LPU Modules"),
        ("mainboard", "mainboards", "Mainboards"),
        ("nic", "nics", "NICs"),
        ("otherfsu", "otherfsus", "Other FSUs"),
        ("psu", "psus", "PSUs"),
        ("rammodule", "rammodules", "RAM Modules"),
    ]

    def buttons(self) -> str:
        """Add button with menu for adding FSUs."""
        user: User | None = getattr(self.context["request"], "user", None)

        buttons: list[str] = []

        if user is not None and user.has_perm("dcim.change_devicetype"):
            buttons.extend(
                [
                    '<div class="btn-group">',
                    '    <button type="button" class="btn btn-primary dropdown-toggle" '
                    'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">',
                    '        <span class="mdi mdi-plus-thick" aria-hidden="true"></span> '
                    'Add FSUs <span class="caret"></span>',
                    "    </button>",
                    '    <ul class="dropdown-menu">',
                ]
            )

            for model_key, tab, label in self.fsu_template_models:
                if user.has_perm(f"nautobot_fsus.add_{model_key}template"):
                    buttons.append(
                        f"        <li><a href=\""
                        f"{reverse(f'plugins:nautobot_fsus:{model_key}template_add')}"
                        f"?device_type={self.obj_pk}"
                        f"&return_url={self.context['object'].get_absolute_url()}"
                        f"%23tab_{tab}\">"
                        f"{label}</a></li>"
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

        self.context["lpumodule_table"] = _fsu_table(
            tables.LPUModuleTemplateTable,
            models.LPUModuleTemplate,
        )
        if user is not None and user.has_perm("nautobot_fsus.change_lpumoduletemplate"):
            self.context["lpumodule_table"].columns.show("pk")

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
            "lpumodules": models.LPUModule.objects.filter(location__pk=self.obj_pk).count(),
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
