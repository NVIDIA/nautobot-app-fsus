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

"""Model serializers for FSU type API endpoints."""
from rest_framework import serializers

from nautobot_fsus.api.mixins import FSUTypeModelSerializer
from nautobot_fsus.models import (
    CPUType,
    DiskType,
    FanType,
    GPUBaseboardType,
    GPUType,
    HBAType,
    MainboardType,
    NICType,
    OtherFSUType,
    PSUType,
    RAMModuleType,
)


class CPUTypeSerializer(FSUTypeModelSerializer):
    """API serializer for CPUType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:cputype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """CPUTypeSerializer model options."""

        model = CPUType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "architecture",
            "cpu_speed",
            "cores",
            "pcie_generation",
            "description",
        ]


class DiskTypeSerializer(FSUTypeModelSerializer):
    """API serializer for DiskType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:disktype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """DiskTypeSerializer model options."""

        model = DiskType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "disk_type",
            "size",
            "description",
        ]


class FanTypeSerializer(FSUTypeModelSerializer):
    """API serializer for FanType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:fantype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """FanTypeSerializer model options."""

        model = FanType


class GPUBaseboardTypeSerializer(FSUTypeModelSerializer):
    """API serializer for GPUBaseboardType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gpubaseboardtype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """GPUBaseboardTypeSerializer model options."""

        model = GPUBaseboardType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "slot_count",
            "description",
        ]


class GPUTypeSerializer(FSUTypeModelSerializer):
    """API serializer for GPUType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gputype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """GPUTypeSerializer model options."""

        model = GPUType


class HBATypeSerializer(FSUTypeModelSerializer):
    """API serializer for HBAType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:hbatype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """HBAType model options."""

        model = HBAType


class MainboardTypeSerializer(FSUTypeModelSerializer):
    """API serializer for MainboardType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:mainboardtype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """MainboardTypeSerializer model options."""

        model = MainboardType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "cpu_socket_count",
            "description",
        ]


class NICTypeSerializer(FSUTypeModelSerializer):
    """API serializer for NICType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:nictype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """NICTypeSerializer model options."""

        model = NICType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "interface_count",
            "description",
        ]


class OtherFSUTypeSerializer(FSUTypeModelSerializer):
    """API serializer for OtherFSUType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:otherfsutype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """OtherFSUTypeSerializer model options."""

        model = OtherFSUType


class PSUTypeSerializer(FSUTypeModelSerializer):
    """API serializer for PSUType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:psutype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """PSUTypeSerializer model options."""

        model = PSUType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "feed_type",
            "power_provided",
            "required_voltage",
            "hot_swappable",
            "description",
        ]


class RAMModuleTypeSerializer(FSUTypeModelSerializer):
    """API serializer for RAMModuleType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:rammoduletype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """RAMModuleTypeSerializer model options."""

        model = RAMModuleType
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "module_type",
            "technology",
            "speed",
            "capacity",
            "quantity",
            "description",
        ]
