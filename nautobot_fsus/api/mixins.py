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

"""Classes to handle user-definable fields and common validations."""
from typing import Any

from nautobot.core.api import WritableNestedSerializer
from nautobot.dcim.api.nested_serializers import (
    NestedDeviceSerializer,
    NestedDeviceTypeSerializer,
    NestedLocationSerializer,
    NestedManufacturerSerializer,
)
from nautobot.extras.api.serializers import (
    NautobotModelSerializer,
    StatusModelSerializerMixin,
    TaggedModelSerializerMixin,
)
from rest_framework import serializers


class FSUModelSerializer(
    NautobotModelSerializer,
    TaggedModelSerializerMixin,
    StatusModelSerializerMixin,
):
    """Extend the standard Nautobot model serializer with FSU-specific validations."""

    device = NestedDeviceSerializer(required=False, allow_null=True)
    location = NestedLocationSerializer(required=False, allow_null=True)

    class Meta:
        """FSUModelSerializer model options."""

        abstract = True
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
        ]

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate the incoming POST/PUT/PATCH data."""
        # FSUs can be assigned to a Device or Location, but not both.
        if data.get("device") is not None and data.get("location") is not None:
            raise serializers.ValidationError(
                "FSUs must be assigned to either a Device or a Storage location, but not both"
            )

        # When changing from a Device to a Storage Location using a PATCH request, only the
        # storage_location field will be present in the data, causing validation to fail because
        # when it runs the FSU will still have a parent Device too...
        if data.get("location") is not None and not data.get("device", False):
            data["device"] = None

        super().validate(data)
        return data


class FSUTemplateModelSerializer(NautobotModelSerializer):
    """Base class for FSU template serializers."""

    device_type = NestedDeviceTypeSerializer()

    class Meta:
        """FSUTemplateModelSerializer model options."""

        abstract = True
        fields = ["id", "url", "name", "fsu_type", "device_type", "description"]


class FSUTypeModelSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """Base class for FSU type serializers."""

    manufacturer = NestedManufacturerSerializer()
    instance_count = serializers.IntegerField(read_only=True)

    class Meta:
        """FSUTypeModelSerializer model options."""

        abstract = True
        fields = [
            "id",
            "url",
            "name",
            "instance_count",
            "manufacturer",
            "part_number",
            "description",
        ]


class NestedFSUSerializer(WritableNestedSerializer):
    """Base class for nested FSU and FSU Template serializers."""

    class Meta:
        """Nested serializer model options."""

        abstract = True
        fields = ["id", "url", "name"]
