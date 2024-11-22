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

from django.core.exceptions import ValidationError as DjangoValidationError
from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin
from rest_framework import serializers
from rest_framework.fields import get_error_detail
from rest_framework.validators import UniqueTogetherValidator


class FSUModelSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """Extend the standard Nautobot model serializer with FSU-specific validations."""

    class Meta:
        """FSUModelSerializer model options."""

        abstract = True
        fields = "__all__"
        extra_kwargs = {
            "device": {"required": False, "allow_null": True},
            "location": {"required": False, "allow_null": True},
        }

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

    def run_validators(self, value):
        """
        Test the given value against all the validators on the field.

        Have to provide our own version of this because FSUs have two unique together constraints,
        but only one of this is valid for any given instance - either (name, device)
        or (name, location). If you try to check both, one of them will always raise an error
        because its field is missing.
        """
        errors = []

        # Add read_only fields with defaults to value before running validators.
        if isinstance(value, dict):
            to_validate = self._read_only_defaults()
            to_validate.update(value)
        else:
            to_validate = value

        # Need to filter the unique together validators to use either the device field or
        # the location field, depending on the parent.
        for validator in self.validators:
            if isinstance(validator, UniqueTogetherValidator):
                if to_validate.get("device") and "location" in validator.fields:
                    continue
                if to_validate.get("location") and "device" in validator.fields:
                    continue
            try:
                if getattr(validator, "requires_context", False):
                    validator(to_validate, self)
                else:
                    validator(to_validate)
            except serializers.ValidationError as exc:
                # If the validation error contains a mapping of fields to
                # errors then simply raise it immediately rather than
                # attempting to accumulate a list of errors.
                if isinstance(exc.detail, dict):
                    raise
                errors.extend(exc.detail)
            except DjangoValidationError as exc:
                errors.extend(get_error_detail(exc))
        if errors:
            raise serializers.ValidationError(errors)


class FSUTemplateModelSerializer(NautobotModelSerializer):
    """Base class for FSU template serializers."""

    class Meta:
        """FSUTemplateModelSerializer model options."""

        abstract = True
        fields = "__all__"


class FSUTypeModelSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    """Base class for FSU type serializers."""

    instance_count = serializers.IntegerField(read_only=True)

    class Meta:
        """FSUTypeModelSerializer model options."""

        abstract = True
        fields = "__all__"
