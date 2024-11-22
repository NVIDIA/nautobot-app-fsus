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

from nautobot.apps.api import ChoiceField
from rest_framework import serializers

from nautobot_fsus import choices
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

    architecture = ChoiceField(choices=choices.CPUArchitectures)

    class Meta(FSUTypeModelSerializer.Meta):
        """CPUTypeSerializer model options."""

        model = CPUType


class DiskTypeSerializer(FSUTypeModelSerializer):
    """API serializer for DiskType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:disktype-detail"
    )

    disk_type = ChoiceField(choices=choices.DiskTypes)

    class Meta(FSUTypeModelSerializer.Meta):
        """DiskTypeSerializer model options."""

        model = DiskType


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


class NICTypeSerializer(FSUTypeModelSerializer):
    """API serializer for NICType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:nictype-detail"
    )

    class Meta(FSUTypeModelSerializer.Meta):
        """NICTypeSerializer model options."""

        model = NICType


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

    feed_type = ChoiceField(choices=choices.PSUFeedType)

    class Meta(FSUTypeModelSerializer.Meta):
        """PSUTypeSerializer model options."""

        model = PSUType


class RAMModuleTypeSerializer(FSUTypeModelSerializer):
    """API serializer for RAMModuleType model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:rammoduletype-detail"
    )

    module_type = ChoiceField(choices=choices.MemoryModuleTypes)
    technology = ChoiceField(choices=choices.MemoryTechnologies)

    class Meta(FSUTypeModelSerializer.Meta):
        """RAMModuleTypeSerializer model options."""

        model = RAMModuleType
