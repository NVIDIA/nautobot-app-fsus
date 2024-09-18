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

"""Extensions to built-in Nautobot filters."""
from django import forms
from nautobot.apps.filters import FilterExtension
from nautobot.utilities.filters import (
    NaturalKeyOrPKMultipleChoiceFilter,
    RelatedMembershipBooleanFilter,
)
from nautobot.utilities.forms.constants import BOOLEAN_WITH_BLANK_CHOICES
from nautobot.utilities.forms.widgets import StaticSelect2

from nautobot_fsus.models import NIC, PSU


class DeviceFilterExtension(FilterExtension):  # pylint: disable=too-few-public-methods
    """Extend the DeviceFilterSet with FSU filter fields."""

    model = "dcim.device"

    filterset_fields = {
        "nautobot_fsus_has_cpus": RelatedMembershipBooleanFilter(
            field_name="cpus",
            label="Has CPUs",
        ),
        "nautobot_fsus_has_disks": RelatedMembershipBooleanFilter(
            field_name="disks",
            label="Has Disks",
        ),
        "nautobot_fsus_has_fans": RelatedMembershipBooleanFilter(
            field_name="fans",
            label="Has Fans",
        ),
        "nautobot_fsus_has_gpus": RelatedMembershipBooleanFilter(
            field_name="gpus",
            label="Has GPUs",
        ),
        "nautobot_fsus_has_gpu_baseboards": RelatedMembershipBooleanFilter(
            field_name="gpubaseboards",
            label="Has GPU Baseboards",
        ),
        "nautobot_fsus_has_hbas": RelatedMembershipBooleanFilter(
            field_name="hbas",
            label="Has HBAs",
        ),
        "nautobot_fsus_has_mainboards": RelatedMembershipBooleanFilter(
            field_name="mainboards",
            label="Has Mainboards",
        ),
        "nautobot_fsus_has_nics": RelatedMembershipBooleanFilter(
            field_name="nics",
            label="Has NICs",
        ),
        "nautobot_fsus_has_otherfsus": RelatedMembershipBooleanFilter(
            field_name="otherfsus",
            label="Has Other FSUs",
        ),
        "nautobot_fsus_has_psus": RelatedMembershipBooleanFilter(
            field_name="psus",
            label="Has PSUs",
        ),
        "nautobot_fsus_has_rammodules": RelatedMembershipBooleanFilter(
            field_name="rammodules",
            label="Has RAM Modules",
        ),
    }

    filterform_fields = {
        "nautobot_fsus_has_gpus": forms.NullBooleanField(
            required=False,
            label="Has GPUs",
            widget=StaticSelect2(choices=BOOLEAN_WITH_BLANK_CHOICES),
        ),
    }


class InterfaceFilterExtension(FilterExtension):  # pylint: disable=too-few-public-methods
    """Extend the InterfaceFilterSet to enable filtering on the parent NIC."""

    model = "dcim.interface"

    filterset_fields = {
        "nautobot_fsus_has_parent_nic": RelatedMembershipBooleanFilter(
            field_name="parent_nic",
            label="Has a Parent NIC",
        ),
        "nautobot_fsus_parent_nic": NaturalKeyOrPKMultipleChoiceFilter(
            field_name="parent_nic",
            to_field_name="name",
            queryset=NIC.objects.all(),
            label="Parent NIC (Name or ID)",
        ),
    }


class LocationFilterExtension(FilterExtension):  # pylint: disable=too-few-public-methods
    """Extend the LocationFilterSet with FSU filter fields."""

    model = "dcim.location"

    filterset_fields = {
        "nautobot_fsus_has_available_cpus": RelatedMembershipBooleanFilter(
            field_name="cpus",
            label="Has available CPUs",
        ),
        "nautobot_fsus_has_available_disks": RelatedMembershipBooleanFilter(
            field_name="disks",
            label="Has available Disks",
        ),
        "nautobot_fsus_has_available_fans": RelatedMembershipBooleanFilter(
            field_name="fans",
            label="Has available Fans",
        ),
        "nautobot_fsus_has_available_gpus": RelatedMembershipBooleanFilter(
            field_name="gpus",
            label="Has available GPUs",
        ),
        "nautobot_fsus_has_available_gpu_baseboards": RelatedMembershipBooleanFilter(
            field_name="gpubaseboards",
            label="Has available GPU Baseboards",
        ),
        "nautobot_fsus_has_available_hbas": RelatedMembershipBooleanFilter(
            field_name="hbas",
            label="Has available HBAs",
        ),
        "nautobot_fsus_has_available_mainboards": RelatedMembershipBooleanFilter(
            field_name="mainboards",
            label="Has available Mainboards",
        ),
        "nautobot_fsus_has_available_nics": RelatedMembershipBooleanFilter(
            field_name="nics",
            label="Has available NICs",
        ),
        "nautobot_fsus_has_available_otherfsus": RelatedMembershipBooleanFilter(
            field_name="otherfsus",
            label="Has available Other FSUs",
        ),
        "nautobot_fsus_has_available_psus": RelatedMembershipBooleanFilter(
            field_name="psus",
            label="Has available PSUs",
        ),
        "nautobot_fsus_has_available_rammodules": RelatedMembershipBooleanFilter(
            field_name="rammodules",
            label="Has available RAM Modules",
        ),
    }


class PowerPortFilterExtension(FilterExtension):  # pylint: disable=too-few-public-methods
    """Extend the PowerPortFilterSet to enable filtering on the parent PSU."""

    model = "dcim.powerport"

    filterset_fields = {
        "nautobot_fsus_has_parent_psu": RelatedMembershipBooleanFilter(
            field_name="parent_psu",
            label="Has a parent PSU",
        ),
        "nautobot_fsus_parent_psu": NaturalKeyOrPKMultipleChoiceFilter(
            field_name="parent_psu",
            to_field_name="name",
            queryset=PSU.objects.all(),
            label="Parent PSU (Name or ID)",
        ),
    }


filter_extensions = [
    DeviceFilterExtension,
    InterfaceFilterExtension,
    LocationFilterExtension,
    PowerPortFilterExtension,
]
