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

"""
Models for Field Serviceable Unit types.

An FSU type is an individual product, defined by manufacturer, model name, and part number.
"""

from django.core.validators import MinValueValidator
from django.db import models
from nautobot.extras.utils import extras_features

from nautobot_fsus import choices
from nautobot_fsus.models.mixins import FSUTypeModel

EXTRAS_FEATURES = (
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "webhooks",
)


@extras_features(*EXTRAS_FEATURES)
class CPUType(FSUTypeModel):
    """Represents a CPU component type."""

    architecture = models.CharField(
        max_length=4,
        choices=choices.CPUArchitectures,
        default=choices.CPUArchitectures.x86,
    )

    cpu_speed = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        help_text="CPU speed in GHz",
    )

    cores = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    pcie_generation = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        choices=choices.PCIeGenerations,
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "CPU Type"
        verbose_name_plural = "CPU Types"


@extras_features(*EXTRAS_FEATURES)
class DiskType(FSUTypeModel):
    """Represents a Disk component type."""

    disk_type = models.CharField(
        max_length=4,
        choices=choices.DiskTypes,
        default=choices.DiskTypes.disk_ssd,
    )

    size = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Disk size, in GB",
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "Disk Type"
        verbose_name_plural = "Disk Types"


@extras_features(*EXTRAS_FEATURES)
class FanType(FSUTypeModel):
    """Represents a Fan component type."""

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "Fan Type"
        verbose_name_plural = "Fan Types"


@extras_features(*EXTRAS_FEATURES)
class GPUBaseboardType(FSUTypeModel):
    """Represents a GPU Baseboard type."""

    slot_count = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="The number of physical GPU slots provided by this GPU Baseboard.",
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "GPU Baseboard Type"
        verbose_name_plural = "GPU Baseboard Types"


@extras_features(*EXTRAS_FEATURES)
class GPUType(FSUTypeModel):
    """Represents a GPU component type."""

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "GPU Type"
        verbose_name_plural = "GPU Types"


@extras_features(*EXTRAS_FEATURES)
class HBAType(FSUTypeModel):
    """Represents an HBA component type."""

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "HBA Type"
        verbose_name_plural = "HBA Types"


@extras_features(*EXTRAS_FEATURES)
class MainboardType(FSUTypeModel):
    """Represents a Mainboard component type."""

    cpu_socket_count = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "Mainboard Type"
        verbose_name_plural = "Mainboard Types"


@extras_features(*EXTRAS_FEATURES)
class NICType(FSUTypeModel):
    """Represents a NIC component type."""

    interface_count = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="The number of physical interfaces provided by the NIC.",
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "NIC Type"
        verbose_name_plural = "NIC Types"


@extras_features(*EXTRAS_FEATURES)
class OtherFSUType(FSUTypeModel):
    """Represents a generic FSU component type."""

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "Other FSU Type"
        verbose_name_plural = "Other FSU Types"


@extras_features(*EXTRAS_FEATURES)
class PSUType(FSUTypeModel):
    """Represents a Power Supply Unit type."""

    feed_type = models.CharField(
        max_length=16,
        choices=choices.PSUFeedType,
        default=choices.PSUFeedType.psu_dc,
    )

    power_provided = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Power provided, in Watts",
    )

    required_voltage = models.CharField(
        max_length=32, blank=True, help_text="Example: `-40V - -72` (DC), `100-240V` (AC)"
    )

    hot_swappable = models.BooleanField(default=False)

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "PSU Type"
        verbose_name_plural = "PSU Types"


@extras_features(*EXTRAS_FEATURES)
class RAMModuleType(FSUTypeModel):
    """Represents a memory component type."""

    module_type = models.CharField(
        max_length=4,
        choices=choices.MemoryModuleTypes,
        default=choices.MemoryModuleTypes.udimm,
    )

    technology = models.CharField(
        max_length=8,
        choices=choices.MemoryTechnologies,
        default=choices.MemoryTechnologies.ddr5,
    )

    speed = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Memory speed in MHz",
    )

    capacity = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        help_text="Memory capacity, in GB",
    )

    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Number of RAM Modules included in part number",
    )

    class Meta(FSUTypeModel.Meta):
        """Metaclass attributes."""

        verbose_name = "RAM Module Type"
        verbose_name_plural = "RAM Module Types"
