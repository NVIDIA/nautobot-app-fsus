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

"""Model serializers for FSU template API endpoints."""

from rest_framework import serializers

from nautobot_fsus.api.mixins import FSUTemplateModelSerializer
from nautobot_fsus.models import (
    CPUTemplate,
    DiskTemplate,
    FanTemplate,
    GPUBaseboardTemplate,
    GPUTemplate,
    HBATemplate,
    MainboardTemplate,
    NICTemplate,
    OtherFSUTemplate,
    PSUTemplate,
    RAMModuleTemplate,
)


class CPUTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for CPUTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:cputemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """CPUTemplateSerializer model options."""

        model = CPUTemplate


class DiskTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for DiskTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:disktemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """DiskTemplateSerializer model options."""

        model = DiskTemplate


class FanTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for FanTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:fantemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """FanTemplateSerializer model options."""

        model = FanTemplate


class GPUBaseboardTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for GPUBaseboardTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gpubaseboardtemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """GPUBaseboardTemplateSerializer model options."""

        model = GPUBaseboardTemplate


class GPUTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for GPUTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:gputemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """GPUTemplateSerializer model options."""

        model = GPUTemplate


class HBATemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for HBATemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:hbatemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """HBTemplateSerializer model options."""

        model = HBATemplate


class MainboardTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for MainboardTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:mainboardtemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """MainboardTemplateSerializer model options."""

        model = MainboardTemplate


class NICTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for NICTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:nictemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """NICTemplateSerializer model options."""

        model = NICTemplate


class OtherFSUTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for OtherFSUTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:otherfsutemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """OtherFSUTemplateSerializer model options."""

        model = OtherFSUTemplate


class PSUTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for PSUTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:psutemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """PSUTemplateSerializer model options."""

        model = PSUTemplate


class RAMModuleTemplateSerializer(FSUTemplateModelSerializer):
    """API serializer for RAMModuleTemplate model."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_fsus-api:rammoduletemplate-detail"
    )

    class Meta(FSUTemplateModelSerializer.Meta):
        """RAMModuleTemplateSerializer model options."""

        model = RAMModuleTemplate
