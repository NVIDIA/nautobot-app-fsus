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

"""Views definitions for the Nautobot FSUs app."""
from typing import Any, Type

from nautobot.core.views import generic
from nautobot.dcim.models import Device, Location

from nautobot_fsus import models, tables
from nautobot_fsus.models.mixins import FSUModel
from nautobot_fsus.tables.mixins import FSUModelTable
from nautobot_fsus.views.fsu_templates import (
    CPUTemplateUIViewSet,
    DiskTemplateUIViewSet,
    FanTemplateUIViewSet,
    GPUBaseboardTemplateUIViewSet,
    GPUTemplateUIViewSet,
    HBATemplateUIViewSet,
    MainboardTemplateUIViewSet,
    NICTemplateUIViewSet,
    OtherFSUTemplateUIViewSet,
    PSUTemplateUIViewSet,
    RAMModuleTemplateUIViewSet,
)
from nautobot_fsus.views.fsu_types import (
    CPUTypeUIViewSet,
    DiskTypeUIViewSet,
    FanTypeUIViewSet,
    GPUBaseboardTypeUIViewSet,
    GPUTypeUIViewSet,
    HBATypeUIViewSet,
    MainboardTypeUIViewSet,
    NICTypeUIViewSet,
    OtherFSUTypeUIViewSet,
    PSUTypeUIViewSet,
    RAMModuleTypeUIViewSet,
)
from nautobot_fsus.views.fsus import (
    CPUBulkRenameView,
    CPUUIViewSet,
    DiskBulkRenameView,
    DiskUIViewSet,
    FanBulkRenameView,
    FanUIViewSet,
    GPUBaseboardBulkRenameView,
    GPUBaseboardUIViewSet,
    GPUBulkRenameView,
    GPUUIViewSet,
    HBABulkRenameView,
    HBAUIViewSet,
    MainboardBulkRenameView,
    MainboardUIViewSet,
    NICBulkRenameView,
    NICUIViewSet,
    OtherFSUBulkRenameView,
    OtherFSUUIViewSet,
    PSUBulkRenameView,
    PSUUIViewSet,
    RAMModuleBulkRenameView,
    RAMModuleUIViewSet,
)


class DeviceFSUViewTab(generic.ObjectView):
    """Tab view for FSUs assigned to a Device."""

    queryset = Device.objects.all()
    template_name = "nautobot_fsus/device_fsu_tab.html"

    def get_extra_context(self, request, instance) -> dict[str, Any]:
        """Add the tables to the view context."""
        def _fsu_table(table: Type[FSUModelTable], fsu: Type[FSUModel]) -> FSUModelTable:
            """Helper method to set up the table for an FSU."""
            fsu_table: FSUModelTable = table(fsu.objects.filter(device__pk=instance.pk))
            fsu_table.columns["actions"].column.extra_context["return_url_extra"] = (
                f"?{request.GET.urlencode()}"
            )
            fsu_table.columns.hide("parent")
            for table_column in ("firmware_version", "driver_name", "driver_version"):
                fsu_table.columns.show(table_column)

            return fsu_table

        context: dict[str, Any] = super().get_extra_context(request, instance)

        context["cpu_table"] = _fsu_table(tables.CPUTable, models.CPU)
        if request.user.has_perm("nautobot_fsus.change_cpu"):
            context["cpu_table"].columns.show("pk")

        context["disk_table"] = _fsu_table(tables.DiskTable, models.Disk)
        if request.user.has_perm("nautobot_fsus.change_disk"):
            context["disk_table"].columns.show("pk")

        context["fan_table"] = _fsu_table(tables.FanTable, models.Fan)
        if request.user.has_perm("nautobot_fsus.change_fan"):
            context["fan_table"].columns.show("pk")

        context["gpu_table"] = _fsu_table(tables.GPUTable, models.GPU)
        if request.user.has_perm("nautobot_fsus.change_gpu"):
            context["gpu_table"].columns.show("pk")

        context["gpubaseboard_table"] = _fsu_table(tables.GPUBaseboardTable, models.GPUBaseboard)
        if request.user.has_perm("nautobot_fsus.change_gpubaseboard"):
            context["gpubaseboard_table"].columns.show("pk")

        context["hba_table"] = _fsu_table(tables.HBATable, models.HBA)
        if request.user.has_perm("nautobot_fsus.change_hba"):
            context["hba_table"].columns.show("pk")

        context["mainboard_table"] = _fsu_table(tables.MainboardTable, models.Mainboard)
        if request.user.has_perm("nautobot_fsus.change_mainboard"):
            context["mainboard_table"].columns.show("pk")

        context["nic_table"] = _fsu_table(tables.NICTable, models.NIC)
        if request.user.has_perm("nautobot_fsus.change_nic"):
            context["nic_table"].columns.show("pk")

        context["otherfsu_table"] = _fsu_table(tables.OtherFSUTable, models.OtherFSU)
        if request.user.has_perm("nautobot_fsus.change_otherfsu"):
            context["otherfsu_table"].columns.show("pk")

        context["psu_table"] = _fsu_table(tables.PSUTable, models.PSU)
        if request.user.has_perm("nautobot_fsus.change_psu"):
            context["psu_table"].columns.show("pk")

        context["rammodule_table"] = _fsu_table(tables.RAMModuleTable, models.RAMModule)
        if request.user.has_perm("nautobot_fsus.change_rammodule"):
            context["rammodule_table"].columns.show("pk")

        return context


class LocationFSUViewTab(generic.ObjectView):
    """Tab view for FSUs assigned to a Location."""

    queryset = Location.objects.all()
    template_name = "nautobot_fsus/location_fsu_tab.html"

    def get_extra_context(self, request, instance) -> dict[str, Any]:
        """Add the tables to the view context."""
        def _fsu_table(table: Type[FSUModelTable], fsu: Type[FSUModel]) -> FSUModelTable:
            """Helper method to set up the table for an FSU."""
            fsu_table: FSUModelTable = table(fsu.objects.filter(location__pk=instance.pk))
            fsu_table.columns["actions"].column.extra_context["return_url_extra"] = (
                f"?{request.GET.urlencode()}"
            )
            fsu_table.columns.hide("parent")
            for table_column in ("firmware_version", "driver_name", "driver_version"):
                fsu_table.columns.show(table_column)

            return fsu_table

        context: dict[str, Any] = super().get_extra_context(request, instance)

        context["cpu_table"] = _fsu_table(tables.CPUTable, models.CPU)
        if request.user.has_perm("nautobot_fsus.change_cpu"):
            context["cpu_table"].columns.show("pk")

        context["disk_table"] = _fsu_table(tables.DiskTable, models.Disk)
        if request.user.has_perm("nautobot_fsus.change_disk"):
            context["disk_table"].columns.show("pk")

        context["fan_table"] = _fsu_table(tables.FanTable, models.Fan)
        if request.user.has_perm("nautobot_fsus.change_fan"):
            context["fan_table"].columns.show("pk")

        context["gpu_table"] = _fsu_table(tables.GPUTable, models.GPU)
        if request.user.has_perm("nautobot_fsus.change_gpu"):
            context["gpu_table"].columns.show("pk")

        context["gpubaseboard_table"] = _fsu_table(tables.GPUBaseboardTable, models.GPUBaseboard)
        if request.user.has_perm("nautobot_fsus.change_gpubaseboard"):
            context["gpubaseboard_table"].columns.show("pk")

        context["hba_table"] = _fsu_table(tables.HBATable, models.HBA)
        if request.user.has_perm("nautobot_fsus.change_hba"):
            context["hba_table"].columns.show("pk")

        context["mainboard_table"] = _fsu_table(tables.MainboardTable, models.Mainboard)
        if request.user.has_perm("nautobot_fsus.change_mainboard"):
            context["mainboard_table"].columns.show("pk")

        context["nic_table"] = _fsu_table(tables.NICTable, models.NIC)
        if request.user.has_perm("nautobot_fsus.change_nic"):
            context["nic_table"].columns.show("pk")

        context["otherfsu_table"] = _fsu_table(tables.OtherFSUTable, models.OtherFSU)
        if request.user.has_perm("nautobot_fsus.change_otherfsu"):
            context["otherfsu_table"].columns.show("pk")

        context["psu_table"] = _fsu_table(tables.PSUTable, models.PSU)
        if request.user.has_perm("nautobot_fsus.change_psu"):
            context["psu_table"].columns.show("pk")

        context["rammodule_table"] = _fsu_table(tables.RAMModuleTable, models.RAMModule)
        if request.user.has_perm("nautobot_fsus.change_rammodule"):
            context["rammodule_table"].columns.show("pk")

        return context


__all__ = (
    "CPUBulkRenameView",
    "CPUTemplateUIViewSet",
    "CPUTypeUIViewSet",
    "CPUUIViewSet",
    "DiskBulkRenameView",
    "DiskTemplateUIViewSet",
    "DiskTypeUIViewSet",
    "DiskUIViewSet",
    "FanBulkRenameView",
    "FanTemplateUIViewSet",
    "FanTypeUIViewSet",
    "FanUIViewSet",
    "GPUBaseboardBulkRenameView",
    "GPUBaseboardTemplateUIViewSet",
    "GPUBaseboardTypeUIViewSet",
    "GPUBaseboardUIViewSet",
    "GPUBulkRenameView",
    "GPUTemplateUIViewSet",
    "GPUTypeUIViewSet",
    "GPUUIViewSet",
    "HBABulkRenameView",
    "HBATemplateUIViewSet",
    "HBATypeUIViewSet",
    "HBAUIViewSet",
    "MainboardBulkRenameView",
    "MainboardTemplateUIViewSet",
    "MainboardTypeUIViewSet",
    "MainboardUIViewSet",
    "NICBulkRenameView",
    "NICTemplateUIViewSet",
    "NICTypeUIViewSet",
    "NICUIViewSet",
    "OtherFSUBulkRenameView",
    "OtherFSUTemplateUIViewSet",
    "OtherFSUTypeUIViewSet",
    "OtherFSUUIViewSet",
    "PSUBulkRenameView",
    "PSUTemplateUIViewSet",
    "PSUTypeUIViewSet",
    "PSUUIViewSet",
    "RAMModuleBulkRenameView",
    "RAMModuleTemplateUIViewSet",
    "RAMModuleTypeUIViewSet",
    "RAMModuleUIViewSet",
)
