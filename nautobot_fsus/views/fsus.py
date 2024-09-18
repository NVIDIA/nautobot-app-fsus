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

"""View definitions for FSU models."""
from typing import Any

from django.db.models import Prefetch
from nautobot.dcim.models import Interface, PowerPort
from nautobot.dcim.tables import DeviceInterfaceTable, DevicePowerPortTable
from nautobot.ipam.models import IPAddress

from nautobot_fsus import filters, forms, models, tables
from nautobot_fsus.api import serializers
from nautobot_fsus.views.mixins import FSUBulkRenameView, FSUModelViewSet


class CPUUIViewSet(FSUModelViewSet):
    """View set for CPU model."""

    bulk_create_form_class = forms.CPUCSVForm
    bulk_update_form_class = forms.CPUBulkEditForm
    filterset_class = filters.CPUFilterSet
    filterset_form_class = forms.CPUFilterForm
    form_class = forms.CPUForm
    lookup_field = "pk"
    queryset = models.CPU.objects.all()
    serializer_class = serializers.CPUSerializer
    table_class = tables.CPUTable
    bulk_table_class = tables.CPUImportTable


class CPUBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming CPU instances."""

    queryset = models.CPU.objects.all()


class DiskUIViewSet(FSUModelViewSet):
    """View set for Disk model."""

    bulk_create_form_class = forms.DiskCSVForm
    bulk_update_form_class = forms.DiskBulkEditForm
    filterset_class = filters.DiskFilterSet
    filterset_form_class = forms.DiskFilterForm
    form_class = forms.DiskForm
    lookup_field = "pk"
    queryset = models.Disk.objects.all()
    serializer_class = serializers.DiskSerializer
    table_class = tables.DiskTable
    bulk_table_class = tables.DiskImportTable


class DiskBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming Disk instances."""

    queryset = models.Disk.objects.all()


class FanUIViewSet(FSUModelViewSet):
    """View set for Fan model."""

    bulk_create_form_class = forms.FanCSVForm
    bulk_update_form_class = forms.FanBulkEditForm
    filterset_class = filters.FanFilterSet
    filterset_form_class = forms.FanFilterForm
    form_class = forms.FanForm
    lookup_field = "pk"
    queryset = models.Fan.objects.all()
    serializer_class = serializers.FanSerializer
    table_class = tables.FanTable
    bulk_table_class = tables.FanImportTable


class FanBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming Fan instances."""

    queryset = models.Fan.objects.all()


class GPUUIViewSet(FSUModelViewSet):
    """View set for GPU model."""

    bulk_create_form_class = forms.GPUCSVForm
    bulk_update_form_class = forms.GPUBulkEditForm
    filterset_class = filters.GPUFilterSet
    filterset_form_class = forms.GPUFilterForm
    form_class = forms.GPUForm
    lookup_field = "pk"
    queryset = models.GPU.objects.all()
    serializer_class = serializers.GPUSerializer
    table_class = tables.GPUTable
    bulk_table_class = tables.GPUImportTable


class GPUBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming GPU instances."""

    queryset = models.GPU.objects.all()


class GPUBaseboardUIViewSet(FSUModelViewSet):
    """View set for GPUBaseboard model."""

    bulk_create_form_class = forms.GPUBaseboardCSVForm
    bulk_update_form_class = forms.GPUBaseboardBulkEditForm
    filterset_class = filters.GPUBaseboardFilterSet
    filterset_form_class = forms.GPUBaseboardFilterForm
    form_class = forms.GPUBaseboardForm
    lookup_field = "pk"
    queryset = models.GPUBaseboard.objects.all()
    serializer_class = serializers.GPUBaseboardSerializer
    table_class = tables.GPUBaseboardTable
    bulk_table_class = tables.GPUBaseboardImportTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add child GPUs to detail view."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "retrieve":
            gpus = models.GPU.objects.restrict(  # type: ignore[attr-defined]
                request.user, "view").filter(
                parent_gpubaseboard=instance)
            gpus_table = tables.GPUTable(data=gpus, user=request.user, orderable=False)
            if (request.user.has_perm("nautobot_fsus.change_gpu")
                    or request.user.has_perm("nautobot_fsus.delete_gpu")):
                gpus_table.columns.show("pk")

            context["gpus_table"] = gpus_table

        return context


class GPUBaseboardBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming GPUBaseboard instances."""

    queryset = models.GPUBaseboard.objects.all()


class HBAUIViewSet(FSUModelViewSet):
    """View set for HBA model."""

    bulk_create_form_class = forms.HBACSVForm
    bulk_update_form_class = forms.HBABulkEditForm
    filterset_class = filters.HBAFilterSet
    filterset_form_class = forms.HBAFilterForm
    form_class = forms.HBAForm
    lookup_field = "pk"
    queryset = models.HBA.objects.all()
    serializer_class = serializers.HBASerializer
    table_class = tables.HBATable
    bulk_table_class = tables.HBAImportTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add child Disks to detail view."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "retrieve":
            disks = models.Disk.objects.restrict(  # type: ignore[attr-defined]
                request.user, "view").filter(parent_hba=instance)
            disks_table = tables.DiskTable(data=disks, user=request.user, orderable=False)
            if (request.user.has_perm("nautobot_fsus.change_disk")
                    or request.user.has_perm("nautobot_fsus.delete_disk")):
                disks_table.columns.show("pk")

            context["disks_table"] = disks_table

        return context


class HBABulkRenameView(FSUBulkRenameView):
    """View for bulk renaming HBA instances."""

    queryset = models.HBA.objects.all()


class MainboardUIViewSet(FSUModelViewSet):
    """View set for Mainboard model."""

    bulk_create_form_class = forms.MainboardCSVForm
    bulk_update_form_class = forms.MainboardBulkEditForm
    filterset_class = filters.MainboardFilterSet
    filterset_form_class = forms.MainboardFilterForm
    form_class = forms.MainboardForm
    lookup_field = "pk"
    queryset = models.Mainboard.objects.all()
    serializer_class = serializers.MainboardSerializer
    table_class = tables.MainboardTable
    bulk_table_class = tables.MainboardImportTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add child CPUs to detail view."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "retrieve":
            cpus = models.CPU.objects.restrict(  # type: ignore[attr-defined]
                request.user, "view").filter(
                parent_mainboard=instance)
            cpus_table = tables.CPUTable(data=cpus, user=request.user, orderable=False)
            if (request.user.has_perm("nautobot_fsus.change_cpu")
                    or request.user.has_perm("nautobot_fsus.delete_cpu")):
                cpus_table.columns.show("pk")

            context["cpus_table"] = cpus_table

        return context


class MainboardBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming Mainboard instances."""

    queryset = models.Mainboard.objects.all()


class NICUIViewSet(FSUModelViewSet):
    """View set for NIC model."""

    bulk_create_form_class = forms.NICCSVForm
    bulk_update_form_class = forms.NICBulkEditForm
    filterset_class = filters.NICFilterSet
    filterset_form_class = forms.NICFilterForm
    form_class = forms.NICForm
    lookup_field = "pk"
    queryset = models.NIC.objects.all()
    serializer_class = serializers.NICSerializer
    table_class = tables.NICTable
    bulk_table_class = tables.NICImportTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add child Interfaces to detail view."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "retrieve":
            interfaces = Interface.objects.restrict(request.user, "view").filter(
                parent_nic=instance
            ).prefetch_related(
                Prefetch("ip_addresses", queryset=IPAddress.objects.restrict(request.user)),
                Prefetch("member_interfaces", queryset=Interface.objects.restrict(request.user)),
                "_path__destination",
                "tags",
            ).select_related("lag", "cable")
            interfaces_table = DeviceInterfaceTable(
                data=interfaces,
                user=request.user,
                orderable=False,
            )
            if (request.user.has_perm("dcim.change_interface")
                    or request.user.has_perm("dcim.delete_interface")):
                interfaces_table.columns.show("pk")

            context["interfaces_table"] = interfaces_table

        return context


class NICBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming NIC instances."""

    queryset = models.NIC.objects.all()


class OtherFSUUIViewSet(FSUModelViewSet):
    """View set for OtherFSU model."""

    bulk_create_form_class = forms.OtherFSUCSVForm
    bulk_update_form_class = forms.OtherFSUBulkEditForm
    filterset_class = filters.OtherFSUFilterSet
    filterset_form_class = forms.OtherFSUFilterForm
    form_class = forms.OtherFSUForm
    lookup_field = "pk"
    queryset = models.OtherFSU.objects.all()
    serializer_class = serializers.OtherFSUSerializer
    table_class = tables.OtherFSUTable
    bulk_table_class = tables.OtherFSUImportTable


class OtherFSUBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming OtherFSU instances."""

    queryset = models.OtherFSU.objects.all()


class PSUUIViewSet(FSUModelViewSet):
    """View set for PSU model."""

    bulk_create_form_class = forms.PSUCSVForm
    bulk_update_form_class = forms.PSUBulkEditForm
    filterset_class = filters.PSUFilterSet
    filterset_form_class = forms.PSUFilterForm
    form_class = forms.PSUForm
    lookup_field = "pk"
    queryset = models.PSU.objects.all()
    serializer_class = serializers.PSUSerializer
    table_class = tables.PSUTable
    bulk_table_class = tables.PSUImportTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add child PowerPorts to detail view."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "retrieve":
            power_ports = PowerPort.objects.restrict(request.user, "view").filter(
                parent_psu=instance).select_related("cable").prefetch_related("_path__destination")
            power_ports_table = DevicePowerPortTable(
                data=power_ports,
                user=request.user,
                orderable=False,
            )
            if (request.user.has_perm("dcim.change_power_port")
                    or request.user.has_perm("dcim.delete_power_port")):
                power_ports_table.columns.show("pk")

            context["power_ports_table"] = power_ports_table

        return context


class PSUBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming PSU instances."""

    queryset = models.PSU.objects.all()


class RAMModuleUIViewSet(FSUModelViewSet):
    """View set for RAMModule model."""

    bulk_create_form_class = forms.RAMModuleCSVForm
    bulk_update_form_class = forms.RAMModuleBulkEditForm
    filterset_class = filters.RAMModuleFilterSet
    filterset_form_class = forms.RAMModuleFilterForm
    form_class = forms.RAMModuleForm
    lookup_field = "pk"
    queryset = models.RAMModule.objects.all()
    serializer_class = serializers.RAMModuleSerializer
    table_class = tables.RAMModuleTable
    bulk_table_class = tables.RAMModuleImportTable


class RAMModuleBulkRenameView(FSUBulkRenameView):
    """View for bulk renaming RAMModule instances."""

    queryset = models.RAMModule.objects.all()
