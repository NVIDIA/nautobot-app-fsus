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

"""Template versions of Field Serviceable Units, to be associated with DeviceTypes."""
from django.db import models
from django.db.models import ForeignKey
from nautobot.dcim.models import Device
from nautobot.extras.utils import extras_features

from nautobot_fsus.models.fsus import (
    CPU,
    Disk,
    Fan,
    GPU,
    GPUBaseboard,
    HBA,
    Mainboard,
    NIC,
    OtherFSU,
    PSU,
    RAMModule,
)
from nautobot_fsus.models.mixins import FSUTemplateModel


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class CPUTemplate(FSUTemplateModel):
    """A template for a CPU to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="CPUType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "CPU Template"
        verbose_name_plural = "CPU Templates"

    def instantiate(self, device: Device) -> CPU:
        """Instantiate a new CPU on a Device."""
        return self._instantiate_model(model=CPU, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class DiskTemplate(FSUTemplateModel):
    """A template for a Disk to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="DiskType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Disk Template"
        verbose_name_plural = "Disk Templates"

    def instantiate(self, device: Device) -> Disk:
        """Instantiate a new Disk on a Device."""
        return self._instantiate_model(model=Disk, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class FanTemplate(FSUTemplateModel):
    """A template for a Fan to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="FanType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Fan Template"
        verbose_name_plural = "Fan Templates"

    def instantiate(self, device: Device) -> Fan:
        """Instantiate a new Fan on a Device."""
        return self._instantiate_model(model=Fan, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class GPUBaseboardTemplate(FSUTemplateModel):
    """A template for a GPU Baseboard to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="GPUBaseboardType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "GPU Baseboard Template"
        verbose_name_plural = "GPU Baseboard Templates"

    def instantiate(self, device: Device) -> GPUBaseboard:
        """Instantiate a new GPU Baseboard on a Device."""
        return self._instantiate_model(model=GPUBaseboard, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class GPUTemplate(FSUTemplateModel):
    """A template for a GPU to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="GPUType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    pci_slot_id = models.CharField(max_length=100, blank=True, verbose_name="PCI slot ID")

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "GPU Template"
        verbose_name_plural = "GPU Templates"

    def instantiate(self, device: Device) -> GPU:
        """Instantiate a new GPU on a Device."""
        return self._instantiate_model(model=GPU, device=device, pci_slot_id=self.pci_slot_id)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class HBATemplate(FSUTemplateModel):
    """A template for a HBA to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="HBAType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    pci_slot_id = models.CharField(max_length=100, blank=True, verbose_name="PCI slot ID")

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "HBA Template"
        verbose_name_plural = "HBA Templates"

    def instantiate(self, device: Device) -> HBA:
        """Instantiate a new HBA on a Device."""
        return self._instantiate_model(model=HBA, device=device, pci_slot_id=self.pci_slot_id)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class MainboardTemplate(FSUTemplateModel):
    """A template for a Mainboard to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="MainboardType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "Mainboard Template"
        verbose_name_plural = "Mainboard Templates"

    def instantiate(self, device: Device) -> Mainboard:
        """Instantiate a new Mainboard on a Device."""
        return self._instantiate_model(model=Mainboard, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class NICTemplate(FSUTemplateModel):
    """A template for a NIC to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="NICType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    pci_slot_id = models.CharField(max_length=100, blank=True, verbose_name="PCI slot ID")

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "NIC Template"
        verbose_name_plural = "NIC Templates"

    def instantiate(self, device: Device) -> NIC:
        """Instantiate a new NIC on a Device."""
        return self._instantiate_model(model=NIC, device=device, pci_slot_id=self.pci_slot_id)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class OtherFSUTemplate(FSUTemplateModel):
    """A template for a generic FSU to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="OtherFSUType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "OtherFSU Template"
        verbose_name_plural = "OtherFSU Templates"

    def instantiate(self, device: Device) -> OtherFSU:
        """Instantiate a new generic FSU on a Device."""
        return self._instantiate_model(model=OtherFSU, device=device)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class PSUTemplate(FSUTemplateModel):
    """A template for a PSU to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="PSUType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    redundant = models.BooleanField(default=False)

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "PSU Template"
        verbose_name_plural = "PSU Templates"

    def instantiate(self, device: Device) -> PSU:
        """Instantiate a new PSU on a Device."""
        return self._instantiate_model(model=PSU, device=device, redundant=self.redundant)


@extras_features("custom_fields", "custom_links", "custom_validators", "relationships")
class RAMModuleTemplate(FSUTemplateModel):
    """A template for a RAM Module to be created on a new device."""

    fsu_type: ForeignKey = models.ForeignKey(
        to="RAMModuleType",
        on_delete=models.PROTECT,
        related_name="templates",
        verbose_name="FSU Type",
    )

    slot_id = models.CharField(max_length=16, blank=True, verbose_name="RAM slot ID")

    class Meta(FSUTemplateModel.Meta):
        """Metaclass attributes."""
        verbose_name = "RAM Module Template"
        verbose_name_plural = "RAM Module Templates"

    def instantiate(self, device: Device) -> RAMModule:
        """Instantiate a new RAM Module on a Device."""
        return self._instantiate_model(model=RAMModule, device=device, slot_id=self.slot_id)
