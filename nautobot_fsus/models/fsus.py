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
Models for Field Serviceable Units (FSUs).

An FSU is a physical instance of its parent FSU type, and can be either installed in a Device,
or available for use in a Location.
"""
from typing import Any

from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from nautobot.extras.utils import extras_features

from nautobot_fsus.models.mixins import FSUModel, PCIFSUModel


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class CPU(FSUModel):
    """Represents an individual CPU component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="CPUType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="CPU Type",
    )

    parent_mainboard: ForeignKey = models.ForeignKey(
        to="Mainboard",
        on_delete=models.PROTECT,
        related_name="cpus",
        blank=True,
        null=True,
    )

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "parent_mainboard",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "CPU"
        verbose_name_plural = "CPUs"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            str(self.device.id if getattr(self, "device", None) else ""),
            str(self.location.id if getattr(self, "location", None) else ""),
            self.name,
            str(self.fsu_type.id),
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.parent_mainboard,
            getattr(self, "asset_tag", ""),
            self.status.slug if getattr(self, "status", None) else "",
            self.description,
            self.comments,
        )


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class Disk(FSUModel):
    """Represents an individual Disk component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="DiskType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="Disk Type",
    )

    parent_hba: ForeignKey = models.ForeignKey(
        to="HBA",
        on_delete=models.PROTECT,
        related_name="disks",
        blank=True,
        null=True,
    )

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "parent_hba",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Disk"
        verbose_name_plural = "Disks"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV data."""
        return (
            str(self.device.id if getattr(self, "device", None) else ""),
            str(self.location.id if getattr(self, "location", None) else ""),
            self.name,
            str(self.fsu_type.id),
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.parent_hba,
            getattr(self, "asset_tag", ""),
            self.status.slug if getattr(self, "status", None) else "",
            self.description,
            self.comments,
        )


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class Fan(FSUModel):
    """Represents an individual Fan component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="FanType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="Fan Type",
    )

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Fan"
        verbose_name_plural = "Fans"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class GPU(PCIFSUModel):
    """Represents an individual GPU component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="GPUType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="GPU Type",
    )

    parent_baseboard: ForeignKey = models.ForeignKey(
        to="GPUBaseboard",
        on_delete=models.PROTECT,
        related_name="gpus",
        blank=True,
        null=True,
    )

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "pci_slot_id",
        "parent_baseboard",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(PCIFSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "GPU"
        verbose_name_plural = "GPUs"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            str(self.device.id if getattr(self, "device", None) else ""),
            str(self.location.id if getattr(self, "location", None) else ""),
            self.name,
            str(self.fsu_type.id),
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.pci_slot_id,
            str(self.parent_baseboard if getattr(self, "parent_baseboard", None) else ""),
            getattr(self, "asset_tag", ""),
            self.status.slug if getattr(self, "status", None) else "",
            self.description,
            self.comments,
        )


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class GPUBaseboard(FSUModel):
    """Represents an individual GPU Baseboard component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="GPUBaseboardType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="GPU Baseboard Type",
    )

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "GPU Baseboard"
        verbose_name_plural = "GPU Baseboards"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class HBA(PCIFSUModel):
    """Represents an individual HBA component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="HBAType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="HBA Type",
    )

    class Meta(PCIFSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "HBA"
        verbose_name_plural = "HBAs"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class Mainboard(FSUModel):
    """Represents an individual Mainboard component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="MainboardType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="Mainboard Type",
    )

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Mainboard"
        verbose_name_plural = "Mainboards"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class NIC(PCIFSUModel):
    """Represents an individual NIC component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="NICType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="NIC Type",
    )

    interfaces: ManyToManyField = models.ManyToManyField(
        to="dcim.Interface",
        related_name="parent_nic",
        blank=True,
    )

    class Meta(PCIFSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "NIC"
        verbose_name_plural = "NICs"


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class OtherFSU(FSUModel):
    """Represents an individual generic FSU component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="OtherFSUType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="Other FSU Type",
    )

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "OtherFSU"
        verbose_name_plural = "OtherFSUs"


class PSU(FSUModel):
    """Represents an individual PSU component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="PSUType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="PSU Type",
    )

    redundant = models.BooleanField(default=False)

    power_ports: ManyToManyField = models.ManyToManyField(
        to="dcim.PowerPort",
        related_name="parent_psu",
        blank=True,
    )

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "redundant",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "PSU"
        verbose_name_plural = "PSUs"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            str(self.device.id if getattr(self, "device", None) else ""),
            str(self.location.id if getattr(self, "location", None) else ""),
            self.name,
            str(self.fsu_type.id),
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            "True" if self.redundant else "False",
            getattr(self, "asset_tag", ""),
            self.status.slug if getattr(self, "status", None) else "",
            self.description,
            self.comments,
        )


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "relationships",
    "statuses",
    "webhooks",
)
class RAMModule(FSUModel):
    """Represents an individual RAM module component in a device or storage location."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="RAMModuleType",
        on_delete=models.PROTECT,
        related_name="instances",
        verbose_name="RAM Module Type",
    )

    slot_id = models.CharField(
        max_length=16,
        blank=True,
        verbose_name="RAM slot ID",
    )

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "slot_id",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        verbose_name = "RAM Module"
        verbose_name_plural = "RAM Modules"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            str(self.device.id if getattr(self, "device", None) else ""),
            str(self.location.id if getattr(self, "location", None) else ""),
            self.name,
            str(self.fsu_type.id),
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.slot_id,
            getattr(self, "asset_tag", ""),
            self.status.slug if getattr(self, "status", None) else "",
            self.description,
            self.comments,
        )
