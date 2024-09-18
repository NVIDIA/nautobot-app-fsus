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

from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse
from nautobot.core.models.generics import PrimaryModel
from nautobot.utilities.fields import NaturalOrderingField

logger = logging.getLogger("nautobot.plugin.fsus")


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
            self.manufacturer.name,
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
