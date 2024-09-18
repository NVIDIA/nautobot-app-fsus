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

"""API endpoint views for the Nautobot FSUs app."""
from nautobot.extras.api.views import NautobotModelViewSet, StatusViewSetMixin

from nautobot_fsus.api import serializers
from nautobot_fsus import filters, models


class CPUAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for CPUs."""

    queryset = models.CPU.objects.all()
    serializer_class = serializers.CPUSerializer
    filterset_class = filters.CPUFilterSet


class CPUTemplateAPIView(NautobotModelViewSet):
    """API view set for CPUTemplates."""

    queryset = models.CPUTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.CPUTemplateSerializer
    filterset_class = filters.CPUTemplateFilterSet


class CPUTypeAPIView(NautobotModelViewSet):
    """API view set for CPUTypes."""

    queryset = models.CPUType.objects.all()
    serializer_class = serializers.CPUTypeSerializer
    filterset_class = filters.CPUTypeFilterSet


class DiskAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for Disks."""

    queryset = models.Disk.objects.all()
    serializer_class = serializers.DiskSerializer
    filterset_class = filters.DiskFilterSet


class DiskTemplateAPIView(NautobotModelViewSet):
    """API view set for DiskTemplates."""

    queryset = models.DiskTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.DiskTemplateSerializer
    filterset_class = filters.DiskTemplateFilterSet


class DiskTypeAPIView(NautobotModelViewSet):
    """API view set for DiskTypes."""

    queryset = models.DiskType.objects.all()
    serializer_class = serializers.DiskTypeSerializer
    filterset_class = filters.DiskTypeFilterSet


class FanAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for Fans."""

    queryset = models.Fan.objects.all()
    serializer_class = serializers.FanSerializer
    filterset_class = filters.FanFilterSet


class FanTemplateAPIView(NautobotModelViewSet):
    """API view set for FanTemplates."""

    queryset = models.FanTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.FanTemplateSerializer
    filterset_class = filters.FanTemplateFilterSet


class FanTypeAPIView(NautobotModelViewSet):
    """API view set for FanTypes."""

    queryset = models.FanType.objects.all()
    serializer_class = serializers.FanTypeSerializer
    filterset_class = filters.FanTypeFilterSet


class GPUAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for GPUs."""

    queryset = models.GPU.objects.all()
    serializer_class = serializers.GPUSerializer
    filterset_class = filters.GPUFilterSet


class GPUBaseboardAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for GPU Baseboards."""

    queryset = models.GPUBaseboard.objects.all()
    serializer_class = serializers.GPUBaseboardSerializer
    filterset_class = filters.GPUBaseboardFilterSet


class GPUBaseboardTemplateAPIView(NautobotModelViewSet):
    """API view set for GPU Baseboard Templates."""

    queryset = models.GPUBaseboardTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.GPUBaseboardTemplateSerializer
    filterset_class = filters.GPUBaseboardTemplateFilterSet


class GPUBaseboardTypeAPIView(NautobotModelViewSet):
    """API view set for GPU Baseboard Types."""

    queryset = models.GPUBaseboardType.objects.all()
    serializer_class = serializers.GPUBaseboardTypeSerializer
    filterset_class = filters.GPUBaseboardTypeFilterSet


class GPUTemplateAPIView(NautobotModelViewSet):
    """API view set for GPUTemplates."""

    queryset = models.GPUTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.GPUTemplateSerializer
    filterset_class = filters.GPUTemplateFilterSet


class GPUTypeAPIView(NautobotModelViewSet):
    """API view set for GPUTypes."""

    queryset = models.GPUType.objects.all()
    serializer_class = serializers.GPUTypeSerializer
    filterset_class = filters.GPUTypeFilterSet


class HBAAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for HBAs."""

    queryset = models.HBA.objects.all()
    serializer_class = serializers.HBASerializer
    filterset_class = filters.HBAFilterSet


class HBATemplateAPIView(NautobotModelViewSet):
    """API view set for HBA Templates."""

    queryset = models.HBATemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.HBATemplateSerializer
    filterset_class = filters.HBATemplateFilterSet


class HBATypeAPIView(NautobotModelViewSet):
    """API view set for HBA Types."""

    queryset = models.HBAType.objects.all()
    serializer_class = serializers.HBATypeSerializer
    filterset_class = filters.HBATypeFilterSet


class MainboardAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for Mainboards."""

    queryset = models.Mainboard.objects.all()
    serializer_class = serializers.MainboardSerializer
    filterset_class = filters.MainboardFilterSet


class MainboardTemplateAPIView(NautobotModelViewSet):
    """API view set for Mainboard Templates."""

    queryset = models.MainboardTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.MainboardTemplateSerializer
    filterset_class = filters.MainboardTemplateFilterSet


class MainboardTypeAPIView(NautobotModelViewSet):
    """API view set for Mainboard Types."""

    queryset = models.MainboardType.objects.all()
    serializer_class = serializers.MainboardTypeSerializer
    filterset_class = filters.MainboardTypeFilterSet


class NICAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for NICs."""

    queryset = models.NIC.objects.all()
    serializer_class = serializers.NICSerializer
    filterset_class = filters.NICFilterSet


class NICTemplateAPIView(NautobotModelViewSet):
    """API view set for NIC Templates."""

    queryset = models.NICTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.NICTemplateSerializer
    filterset_class = filters.NICTemplateFilterSet


class NICTypeAPIView(NautobotModelViewSet):
    """API view set for NIC Types."""

    queryset = models.NICType.objects.all()
    serializer_class = serializers.NICTypeSerializer
    filterset_class = filters.NICTypeFilterSet


class OtherFSUAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for Other FSUs."""

    queryset = models.OtherFSU.objects.all()
    serializer_class = serializers.OtherFSUSerializer
    filterset_class = filters.OtherFSUFilterSet


class OtherFSUTemplateAPIView(NautobotModelViewSet):
    """API view set for Other FSU Templates."""

    queryset = models.OtherFSUTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.OtherFSUTemplateSerializer
    filterset_class = filters.OtherFSUTemplateFilterSet


class OtherFSUTypeAPIView(NautobotModelViewSet):
    """API view set for Other FSU Types."""

    queryset = models.OtherFSUType.objects.all()
    serializer_class = serializers.OtherFSUTypeSerializer
    filterset_class = filters.OtherFSUTypeFilterSet


class PSUAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for PSUs."""

    queryset = models.PSU.objects.all()
    serializer_class = serializers.PSUSerializer
    filterset_class = filters.PSUFilterSet


class PSUTemplateAPIView(NautobotModelViewSet):
    """API view set for PSU Templates."""

    queryset = models.PSUTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.PSUTemplateSerializer
    filterset_class = filters.PSUTemplateFilterSet


class PSUTypeAPIView(NautobotModelViewSet):
    """API view set for PSU Types."""

    queryset = models.PSUType.objects.all()
    serializer_class = serializers.PSUTypeSerializer
    filterset_class = filters.PSUTypeFilterSet


class RAMModuleAPIView(NautobotModelViewSet, StatusViewSetMixin):
    """API view set for RAM Modules."""

    queryset = models.RAMModule.objects.all()
    serializer_class = serializers.RAMModuleSerializer
    filterset_class = filters.RAMModuleFilterSet


class RAMModuleTemplateAPIView(NautobotModelViewSet):
    """API view set for RAM Module Templates."""

    queryset = models.RAMModuleTemplate.objects.select_related("device_type__manufacturer")
    serializer_class = serializers.RAMModuleTemplateSerializer
    filterset_class = filters.RAMModuleTemplateFilterSet


class RAMModuleTypeAPIView(NautobotModelViewSet):
    """API view set for RAM Module Types."""

    queryset = models.RAMModuleType.objects.all()
    serializer_class = serializers.RAMModuleTypeSerializer
    filterset_class = filters.RAMModuleTypeFilterSet
