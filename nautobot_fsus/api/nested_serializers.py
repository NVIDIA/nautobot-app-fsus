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

"""Nested model serializers for API responses."""
from rest_framework.relations import HyperlinkedIdentityField

from nautobot_fsus import models
from nautobot_fsus.api.mixins import NestedFSUSerializer


class NestedCPUSerializer(NestedFSUSerializer):
    """Nested CPU serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:cpu-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedCPUSerializer model options."""

        model = models.CPU


class NestedCPUTemplateSerializer(NestedFSUSerializer):
    """Nested CPUTemplate serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:cputemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedCPUTemplateSerializer model options."""

        model = models.CPUTemplate


class NestedCPUTypeSerializer(NestedFSUSerializer):
    """Nested CPUType serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:cputype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedCPUTypeSerializer model options."""

        model = models.CPUType
        fields = ["id", "url", "name", "part_number"]


class NestedDiskSerializer(NestedFSUSerializer):
    """Nested Disk serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:disk-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedDiskSerializer model options."""

        model = models.Disk


class NestedDiskTemplateSerializer(NestedFSUSerializer):
    """Nested Disk Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:disktemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedDiskTemplateSerializer model options."""

        model = models.DiskTemplate


class NestedDiskTypeSerializer(NestedFSUSerializer):
    """Nested Disk Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:disktype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedDiskTypeSerializer model options."""

        model = models.DiskType
        fields = ["id", "url", "name", "part_number"]


class NestedFanSerializer(NestedFSUSerializer):
    """Nested Fan serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:fan-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedFanSerializer model options."""

        model = models.Fan


class NestedFanTemplateSerializer(NestedFSUSerializer):
    """Nested Fan Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:fantemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedFanTemplateSerializer model options."""

        model = models.FanTemplate


class NestedFanTypeSerializer(NestedFSUSerializer):
    """Nested Fan Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:fantype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedFanTypeSerializer model options."""

        model = models.FanType
        fields = ["id", "url", "name", "part_number"]


class NestedGPUBaseboardSerializer(NestedFSUSerializer):
    """Nested GPU Baseboard serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gpubaseboard-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUBaseboardSerializer model options."""

        model = models.GPUBaseboard


class NestedGPUBaseboardTemplateSerializer(NestedFSUSerializer):
    """Nested GPU Baseboard Template serializer."""

    url = HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gpubaseboardtemplate-detail"
    )

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUBaseboardTemplateSerializer model options."""

        model = models.GPUBaseboardTemplate


class NestedGPUBaseboardTypeSerializer(NestedFSUSerializer):
    """Nested GPU Baseboard Type serializer."""

    url = HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gpubaseboardtype-detail"
    )

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUBaseboardTypeSerializer model options."""

        model = models.GPUBaseboardType
        fields = ["id", "url", "name", "part_number"]


class NestedGPUSerializer(NestedFSUSerializer):
    """Nested GPU serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gpu-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUSerializer model options."""

        model = models.GPU


class NestedGPUTemplateSerializer(NestedFSUSerializer):
    """Nested GPU Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gputemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUTemplateSerializer model options."""

        model = models.GPUTemplate


class NestedGPUTypeSerializer(NestedFSUSerializer):
    """Nested GPU Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gputype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedGPUTypeSerializer model options."""

        model = models.GPUType
        fields = ["id", "url", "name", "part_number"]


class NestedHBASerializer(NestedFSUSerializer):
    """Nested HBA serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:hba-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedHBASerializer model options."""

        model = models.HBA


class NestedHBATemplateSerializer(NestedFSUSerializer):
    """Nested HBA Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:hbatemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedHBATemplateSerializer model options."""

        model = models.HBATemplate


class NestedHBATypeSerializer(NestedFSUSerializer):
    """Nested HBA Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:hbatype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedHBATypeSerializer model options."""

        model = models.HBAType
        fields = ["id", "url", "name", "part_number"]


class NestedMainboardSerializer(NestedFSUSerializer):
    """Nested Mainboard serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:mainboard-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedMainboardSerializer model options."""

        model = models.Mainboard


class NestedMainboardTemplateSerializer(NestedFSUSerializer):
    """Nested Mainboard Template serializer."""

    url = HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:mainboardtemplate-detail"
    )

    class Meta(NestedFSUSerializer.Meta):
        """NestedMainboardTemplateSerializer model options."""

        model = models.MainboardTemplate


class NestedMainboardTypeSerializer(NestedFSUSerializer):
    """Nested Mainboard Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:mainboardtype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedMainboardTypeSerializer model options."""

        model = models.MainboardType
        fields = ["id", "url", "name", "part_number"]


class NestedNICSerializer(NestedFSUSerializer):
    """Nested NIC serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:nic-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedNICSerializer model options."""

        model = models.NIC


class NestedNICTemplateSerializer(NestedFSUSerializer):
    """Nested NIC Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:nictemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedNICTemplateSerializer model options."""

        model = models.NICTemplate


class NestedNICTypeSerializer(NestedFSUSerializer):
    """Nested NIC Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:nictype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedNICTypeSerializer model options."""

        model = models.NICType
        fields = ["id", "url", "name", "part_number"]


class NestedOtherFSUSerializer(NestedFSUSerializer):
    """Nested Other FSU serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:otherfsu-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedOtherFSUSerializer model options."""

        model = models.OtherFSU


class NestedOtherFSUTemplateSerializer(NestedFSUSerializer):
    """Nested Other FSU Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:otherfsutemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedOtherFSUTemplateSerializer model options."""

        model = models.OtherFSUTemplate


class NestedOtherFSUTypeSerializer(NestedFSUSerializer):
    """Nested Other FSU Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:otherfsutype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedOtherFSUTypeSerializer model options."""

        model = models.OtherFSUType
        fields = ["id", "url", "name", "part_number"]


class NestedPSUSerializer(NestedFSUSerializer):
    """Nested PSU serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:psu-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedPSUSerializer model options."""

        model = models.PSU


class NestedPSUTemplateSerializer(NestedFSUSerializer):
    """Nested PSU Template serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:psutemplate-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedPSUSerializer model options."""

        model = models.PSUTemplate


class NestedPSUTypeSerializer(NestedFSUSerializer):
    """Nested PSU Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:psutype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedPSUTypeSerializer model options."""

        model = models.PSUType
        fields = ["id", "url", "name", "part_number"]


class NestedRAMModuleSerializer(NestedFSUSerializer):
    """Nested RAM Module serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:rammodule-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedRAMModuleSerializer model options."""

        model = models.RAMModule


class NestedRAMModuleTemplateSerializer(NestedFSUSerializer):
    """Nested RAM Module Template serializer."""

    url = HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:rammoduletemplate-detail"
    )

    class Meta(NestedFSUSerializer.Meta):
        """NestedRAMModuleTemplateSerializer model options."""

        model = models.RAMModuleTemplate


class NestedRAMModuleTypeSerializer(NestedFSUSerializer):
    """Nested RAM Module Type serializer."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:rammoduletype-detail")

    class Meta(NestedFSUSerializer.Meta):
        """NestedRAMModuleTypeSerializer model options."""

        model = models.RAMModuleType
        fields = ["id", "url", "name", "part_number"]
