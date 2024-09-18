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

"""View definitions for FSUType models."""
from typing import Any

from django.urls import reverse

from nautobot_fsus import filters, forms, models, tables
from nautobot_fsus.api import serializers
from nautobot_fsus.views.mixins import FSUTypeModelViewSet


class CPUTypeUIViewSet(FSUTypeModelViewSet):
    """View set for CPUType model."""

    bulk_create_form_class = forms.CPUTypeCSVForm
    bulk_update_form_class = forms.CPUTypeBulkEditForm
    filterset_class = filters.CPUTypeFilterSet
    filterset_form_class = forms.CPUTypeFilterForm
    form_class = forms.CPUTypeForm
    lookup_field = "pk"
    queryset = models.CPUType.objects.all()
    serializer_class = serializers.CPUTypeSerializer
    table_class = tables.CPUTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:cpu_list")
        context["instance_count"] = models.CPU.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class DiskTypeUIViewSet(FSUTypeModelViewSet):
    """View set for DiskType model."""

    bulk_create_form_class = forms.DiskTypeCSVForm
    bulk_update_form_class = forms.DiskTypeBulkEditForm
    filterset_class = filters.DiskTypeFilterSet
    filterset_form_class = forms.DiskTypeFilterForm
    form_class = forms.DiskTypeForm
    lookup_field = "pk"
    queryset = models.DiskType.objects.all()
    serializer_class = serializers.DiskTypeSerializer
    table_class = tables.DiskTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:disk_list")
        context["instance_count"] = models.Disk.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class FanTypeUIViewSet(FSUTypeModelViewSet):
    """View set for FanType model."""

    bulk_create_form_class = forms.FanTypeCSVForm
    bulk_update_form_class = forms.FanTypeBulkEditForm
    filterset_class = filters.FanTypeFilterSet
    filterset_form_class = forms.FanTypeFilterForm
    form_class = forms.FanTypeForm
    lookup_field = "pk"
    queryset = models.FanType.objects.all()
    serializer_class = serializers.FanTypeSerializer
    table_class = tables.FanTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:fan_list")
        context["instance_count"] = models.Fan.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class GPUTypeUIViewSet(FSUTypeModelViewSet):
    """View set for GPUType model."""

    bulk_create_form_class = forms.GPUTypeCSVForm
    bulk_update_form_class = forms.GPUTypeBulkEditForm
    filterset_class = filters.GPUTypeFilterSet
    filterset_form_class = forms.GPUTypeFilterForm
    form_class = forms.GPUTypeForm
    lookup_field = "pk"
    queryset = models.GPUType.objects.all()
    serializer_class = serializers.GPUTypeSerializer
    table_class = tables.GPUTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:gpu_list")
        context["instance_count"] = models.GPU.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class GPUBaseboardTypeUIViewSet(FSUTypeModelViewSet):
    """View set for GPUBaseboardType model."""

    bulk_create_form_class = forms.GPUBaseboardTypeCSVForm
    bulk_update_form_class = forms.GPUBaseboardTypeBulkEditForm
    filterset_class = filters.GPUBaseboardTypeFilterSet
    filterset_form_class = forms.GPUBaseboardTypeFilterForm
    form_class = forms.GPUBaseboardTypeForm
    lookup_field = "pk"
    queryset = models.GPUBaseboardType.objects.all()
    serializer_class = serializers.GPUBaseboardTypeSerializer
    table_class = tables.GPUBaseboardTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:gpubaseboard_list")
        context["instance_count"] = models.GPUBaseboard.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class HBATypeUIViewSet(FSUTypeModelViewSet):
    """View set for HBAType model."""

    bulk_create_form_class = forms.HBATypeCSVForm
    bulk_update_form_class = forms.HBATypeBulkEditForm
    filterset_class = filters.HBATypeFilterSet
    filterset_form_class = forms.HBATypeFilterForm
    form_class = forms.HBATypeForm
    lookup_field = "pk"
    queryset = models.HBAType.objects.all()
    serializer_class = serializers.HBATypeSerializer
    table_class = tables.HBATypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:hba_list")
        context["instance_count"] = models.HBA.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class MainboardTypeUIViewSet(FSUTypeModelViewSet):
    """View set for MainboardType model."""

    bulk_create_form_class = forms.MainboardTypeCSVForm
    bulk_update_form_class = forms.MainboardTypeBulkEditForm
    filterset_class = filters.MainboardTypeFilterSet
    filterset_form_class = forms.MainboardTypeFilterForm
    form_class = forms.MainboardTypeForm
    lookup_field = "pk"
    queryset = models.MainboardType.objects.all()
    serializer_class = serializers.MainboardTypeSerializer
    table_class = tables.MainboardTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:mainboard_list")
        context["instance_count"] = models.Mainboard.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class NICTypeUIViewSet(FSUTypeModelViewSet):
    """View set for NICType model."""

    bulk_create_form_class = forms.NICTypeCSVForm
    bulk_update_form_class = forms.NICTypeBulkEditForm
    filterset_class = filters.NICTypeFilterSet
    filterset_form_class = forms.NICTypeFilterForm
    form_class = forms.NICTypeForm
    lookup_field = "pk"
    queryset = models.NICType.objects.all()
    serializer_class = serializers.NICTypeSerializer
    table_class = tables.NICTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:nic_list")
        context["instance_count"] = models.NIC.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class OtherFSUTypeUIViewSet(FSUTypeModelViewSet):
    """View set for OtherFSUType model."""

    bulk_create_form_class = forms.OtherFSUTypeCSVForm
    bulk_update_form_class = forms.OtherFSUTypeBulkEditForm
    filterset_class = filters.OtherFSUTypeFilterSet
    filterset_form_class = forms.OtherFSUTypeFilterForm
    form_class = forms.OtherFSUTypeForm
    lookup_field = "pk"
    queryset = models.OtherFSUType.objects.all()
    serializer_class = serializers.OtherFSUTypeSerializer
    table_class = tables.OtherFSUTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:otherfsu_list")
        context["instance_count"] = models.OtherFSU.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class PSUTypeUIViewSet(FSUTypeModelViewSet):
    """View set for PSUType model."""

    bulk_create_form_class = forms.PSUTypeCSVForm
    bulk_update_form_class = forms.PSUTypeBulkEditForm
    filterset_class = filters.PSUTypeFilterSet
    filterset_form_class = forms.PSUTypeFilterForm
    form_class = forms.PSUTypeForm
    lookup_field = "pk"
    queryset = models.PSUType.objects.all()
    serializer_class = serializers.PSUTypeSerializer
    table_class = tables.PSUTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:psu_list")
        context["instance_count"] = models.PSU.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context


class RAMModuleTypeUIViewSet(FSUTypeModelViewSet):
    """View set for RAMModuleType model."""

    bulk_create_form_class = forms.RAMModuleTypeCSVForm
    bulk_update_form_class = forms.RAMModuleTypeBulkEditForm
    filterset_class = filters.RAMModuleTypeFilterSet
    filterset_form_class = forms.RAMModuleTypeFilterForm
    form_class = forms.RAMModuleTypeForm
    lookup_field = "pk"
    queryset = models.RAMModuleType.objects.all()
    serializer_class = serializers.RAMModuleTypeSerializer
    table_class = tables.RAMModuleTypeTable

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add extra template date to the context."""
        context: dict[str, Any] = super().get_extra_context(request, instance)
        context["fsu_list"] = reverse("plugins:nautobot_fsus:rammodule_list")
        context["instance_count"] = models.RAMModule.objects.restrict(  # type: ignore[attr-defined]
            request.user).filter(fsu_type=instance).count()

        return context
