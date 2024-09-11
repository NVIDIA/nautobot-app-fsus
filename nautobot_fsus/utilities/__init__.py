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

"""Helpful utility methods."""
from django.core.exceptions import ValidationError
from nautobot.dcim.models import Device
from nautobot.dcim.models.device_components import ComponentModel

from nautobot_fsus.models.mixins import FSUModel


def validate_parent_device(
    fsus: list[FSUModel | ComponentModel],
    parent_device: Device | None
) -> None:
    """
    Ensure that child FSUs set for a parent instance are assigned to the same Device.

    Args:
        fsus (list[FSUModel]): List of FSU units being assigned to the parent instance.
        parent_device (Device): Parent Device the instance is assigned to.
    """
    # Gotta have a parent device
    if parent_device is None:
        raise ValidationError(
            "Parent FSU must be assigned to a device in order to add child FSUs"
        )

    # All child FSUs must be assigned to the same parent Device as the instance.
    for fsu in fsus:
        if fsu.device != parent_device:
            raise ValidationError(
                f"{fsu._meta.verbose_name} {fsu.name} has a different parent device "
                f"({getattr(fsu.device, 'name', 'No device set')}) than that of its "
                f"parent FSU ({parent_device.name})"
            )
