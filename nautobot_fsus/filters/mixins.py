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

"""Mixin classes to support user-definable fields in model filters."""
import django_filters
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer
from nautobot.utilities.filters import (
    NaturalKeyOrPKMultipleChoiceFilter,
    MultiValueCharFilter,
    MultiValueUUIDFilter,
    RelatedMembershipBooleanFilter,
    SearchFilter,
    TagFilter,
)


class FSUModelFilterSetMixin(django_filters.FilterSet):
    """Mixin with the common filter code for FSUs."""
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "fsu_type__name": "icontains",
            "serial": "icontains",
            "firmware": "icontains",
            "driver_name": "icontains",
            "driver": "icontains",
        }
    )

    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name",
        queryset=Device.objects.all(),
        to_field_name="name",
        label="Device",
    )

    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label="Device (ID)",
    )

    location = django_filters.ModelMultipleChoiceFilter(
        field_name="location__name",
        queryset=Location.objects.all(),
        to_field_name="name",
        label="Storage Location",
    )

    location_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Location.objects.all(),
        label="Storage Location (ID)",
    )

    tags = TagFilter()


class FSUTemplateModelFilterSetMixin(django_filters.FilterSet):
    """Mixin with the common filter code for FSU templates."""
    q = SearchFilter(filter_predicates={"name": "icontains"})

    device_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        field_name="device_type_id",
        label="Device Type (ID)",
    )

    device_type = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=DeviceType.objects.all(),
        label="Device type (slug or ID)",
    )

    id = MultiValueUUIDFilter(label="ID")
    name = MultiValueCharFilter(label="Name")
    description = MultiValueCharFilter(label="Description")


class FSUTypeModelFilterSetMixin(django_filters.FilterSet):
    """Mixin with the common filter code for FSU types."""
    q = SearchFilter(
        filter_predicates={
            "manufacturer__name": "icontains",
            "name": "icontains",
            "part_number": "icontains",
            "description": "icontains",
            "comments": "icontains",
        }
    )

    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name="manufacturer__name",
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        label="Manufacturer",
    )

    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Manufacturer.objects.all(),
        label="Manufacturer (ID)",
    )

    has_instances = RelatedMembershipBooleanFilter(
        field_name="instances",
        label="Has Instances",
    )

    tags = TagFilter()
