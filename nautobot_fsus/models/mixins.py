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

"""Base classes for object models."""
import logging
from typing import Any

from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse
from nautobot.core.models.generics import PrimaryModel
from nautobot.dcim.models import Device, Location
from nautobot.extras.models import StatusModel
from nautobot.extras.models.change_logging import ObjectChange
from nautobot.utilities.fields import NaturalOrderingField

logger = logging.getLogger("nautobot.plugin.fsus")


class FSUModel(PrimaryModel, StatusModel):
    """
    Abstract base class for Field Serviceable Units.

    An FSU is a physical device component that is being tracked in inventory. All FSUs have
    an FSU type, relating them to their manufacturer, model name, and part number. FSUs are also
    related to either the Device where they are installed, or to a Location if they are in
    storage and not yet installed. In addition, this abstract class provides the common set
    of data fields all FSUs share - name, serial number, firmware version, etc.
    """

    fsu_type: ForeignKey

    device: ForeignKey = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        blank=True,
        null=True,
        help_text="Device the FSU is installed in - an FSU requires either a parent Device "
                  "or a parent Location."
    )

    location: ForeignKey = models.ForeignKey(
        to="dcim.Location",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        blank=True,
        null=True,
        help_text="Location where the FSU is stored - an FSU requires either a parent Device "
                  "or a parent Location."
    )

    name = models.CharField(max_length=100, db_index=True)
    _name = NaturalOrderingField(target_field="name", max_length=255, blank=True, db_index=True)

    serial_number = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Serial number",
        db_index=True,
    )

    firmware_version = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="Firmware version",
    )

    driver_version = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="Driver version",
    )

    driver_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Driver name",
    )

    asset_tag = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Asset tag",
        help_text="A unique tag used to identify this FSU.",
    )

    description = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)

    clone_fields = [
        "fsu_type",
        "device",
        "location",
        "firmware_version",
        "driver_version",
        "driver_name",
    ]

    csv_headers = [
        "device",
        "location",
        "name",
        "fsu_type",
        "serial_number",
        "firmware_version",
        "driver_version",
        "driver_name",
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta:
        """Metaclass attributes."""
        abstract = True
        ordering = ["device", "location", "_name"]
        unique_together = [["device", "name"], ["location", "name"]]

    def __str__(self) -> str:
        """Default string representation of the FSU."""
        return str(self.name)

    @property
    def parent(self) -> Device | Location | None:
        """Return the parent Device or Location, as appropriate."""
        if self.device and isinstance(self.device, Device):
            return self.device
        if self.location and isinstance(self.location, Location):
            return self.location

        return None

    def to_objectchange(self, action: str, **kwargs: Any) -> ObjectChange:
        """
        Return a new ObjectChange on updates.

        ObjectChange will have `related_object` set to either the parent `device`
        or `location` as appropriate.
        """
        related_object: Device | Location | None = self.parent

        return super().to_objectchange(action, related_object=related_object, **kwargs)

    def save(self, *args, **kwargs) -> None:
        """Save the FSU object to the database."""
        if self.device and self.location:
            self.location = None  # type: ignore

        super().save(*args, **kwargs)

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            self.device.id,
            self.location.id,
            self.name,
            self.fsu_type.id,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )

    def get_absolute_url(self) -> str:
        """Calculate the absolute URL of the FSU instance."""
        return reverse(f"plugins:fsus:{self._meta.model_name}", kwargs={"pk": self.pk})


class FSUTypeModel(PrimaryModel):
    """
    Abstract base class for FSU types.

    An FSU type is a discrete component, with a manufacturer, model name, and part number.
    It is equivalent to a catalog entry for a product that can be purchased. Each FSU type
    has a unique part number for its manufacturer.
    """

    manufacturer: ForeignKey = models.ForeignKey(
        to="dcim.Manufacturer",
        on_delete=models.PROTECT,
        related_name="%(class)ss",
    )

    name = models.CharField(max_length=100, verbose_name="Model Name")
    _name = NaturalOrderingField(target_field="name", max_length=255, blank=True, db_index=True)
    part_number = models.CharField(max_length=100, verbose_name="Part Number")
    description = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)

    clone_fields = ["manufacturer", "name"]
    csv_headers = ["manufacturer", "name", "part_number", "description", "comments"]

    class Meta:
        """Metaclass attributes."""
        abstract = True
        ordering = ["manufacturer", "_name", "part_number"]
        unique_together = ["manufacturer", "part_number"]

    def __str__(self) -> str:
        """String representation of the FSU type."""
        return f"{self.name}"

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of values suitable for CSV export."""
        return (
            self.manufacturer.id,
            self.name,
            self.part_number,
            self.description,
            self.comments
        )

    @property
    def display(self) -> str:
        """Display string for an FSU type - manufacturer, name, and part number."""
        return f"{self.manufacturer.name} {self.name} [{self.part_number}]"

    def get_absolute_url(self) -> str:
        """Calculate the absolute URL for an FSU type."""
        return reverse(f"plugins:fsus:{self._meta.model_name}", kwargs={"pk": self.pk})


class PCIFSUModel(FSUModel):
    """Abstract base class for an FSU that occupies a PCI slot."""

    pci_slot_id = models.CharField(max_length=100, blank=True, verbose_name="PCI slot ID")

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
        "asset_tag",
        "status",
        "description",
        "comments",
    ]

    class Meta(FSUModel.Meta):
        """Metaclass attributes."""
        abstract = True

    def to_csv(self) -> tuple[str, ...]:
        """Return a tuple of model values suitable for CSV export."""
        return (
            self.device.id,
            self.location.id,
            self.name,
            self.fsu_type.id,
            self.serial_number,
            self.firmware_version,
            self.driver_version,
            self.driver_name,
            self.pci_slot_id,
            self.asset_tag,
            self.status,
            self.description,
            self.comments,
        )
