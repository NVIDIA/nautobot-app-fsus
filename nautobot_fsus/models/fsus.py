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
from copy import copy

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from nautobot.extras.utils import extras_features

from nautobot_fsus.models.mixins import FSUModel, PCIFSUModel
from nautobot_fsus.utilities import validate_parent_device


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
            self.device.identifier if self.device else "",  # pylint: disable=no-member
            self.location.name if self.location else "",
            self.name,
            self.fsu_type.name,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.parent_mainboard.name if self.parent_mainboard else "",
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )

    def clean_fields(self, exclude=None) -> None:
        """Validate the parent Device against the parent Mainboard."""
        super().clean_fields(exclude=exclude)

        parent_mainboard: Mainboard
        if parent_mainboard := copy(self.parent_mainboard):
            errors = {}

            try:
                validate_parent_device([self], parent_mainboard.device)
            except ValidationError as error:
                errors["parent_mainboard"] = error.error_list

            if socket_count := parent_mainboard.fsu_type.cpu_socket_count:
                cpu_count = parent_mainboard.cpus.count()
                if self not in parent_mainboard.cpus.all() and cpu_count >= socket_count:
                    errors.setdefault("parent_mainboard", [])
                    errors["parent_mainboard"].extend(
                        ValidationError("Mainboard has no available CPU sockets.").error_list
                    )

            if errors:
                raise ValidationError(errors)


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
            self.device.identifier if self.device else "",  # pylint: disable=no-member
            self.location.name if self.location else "",
            self.name,
            self.fsu_type.name,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.parent_hba.name if self.parent_hba else "",
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )

    def clean_fields(self, exclude=None) -> None:
        """Validate the parent Device against the parent HBA."""
        super().clean_fields(exclude=exclude)

        parent_hba: HBA
        if parent_hba := copy(self.parent_hba):
            try:
                validate_parent_device([self], parent_hba.device)
            except ValidationError as error:
                raise ValidationError({"parent_hba": error.error_list}) from error


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

    parent_gpubaseboard: ForeignKey = models.ForeignKey(
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
        "parent_gpubaseboard",
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
            self.device.identifier if self.device else "",  # pylint: disable=no-member
            self.location.name if self.location else "",
            self.name,
            self.fsu_type.name,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.pci_slot_id,
            self.parent_gpubaseboard.name if self.parent_gpubaseboard else "",
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )

    def clean_fields(self, exclude=None) -> None:
        """Validate the parent Device against the parent GPU Baseboard."""
        super().clean_fields(exclude=exclude)

        # if self.parent_gpubaseboard is not None:
        parent_gpubaseboard: GPUBaseboard
        if parent_gpubaseboard := copy(self.parent_gpubaseboard):
            errors = {}

            try:
                validate_parent_device([self], parent_gpubaseboard.device)
            except ValidationError as error:
                errors["parent_gpubaseboard"] = error.error_list

            if slot_count := parent_gpubaseboard.fsu_type.slot_count:
                gpu_count = parent_gpubaseboard.gpus.count()
                if self not in parent_gpubaseboard.gpus.all() and gpu_count >= slot_count:
                    errors.setdefault("parent_gpubaseboard", [])
                    errors["parent_gpubaseboard"].extend(
                        ValidationError("GPU Baseboard has no available slots.").error_list
                    )

            if errors:
                raise ValidationError(errors)


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
        limit_choices_to={"type__n": ["bridge", "lag", "virtual"]},
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
            self.device.identifier if self.device else "",  # pylint: disable=no-member
            self.location.name if self.location else "",
            self.name,
            self.fsu_type.name,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            str(self.redundant),
            self.asset_tag,
            self.status,
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
            self.device.identifier if self.device else "",  # pylint: disable=no-member
            self.location.name if self.location else "",
            self.name,
            self.fsu_type.name,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.slot_id,
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )
