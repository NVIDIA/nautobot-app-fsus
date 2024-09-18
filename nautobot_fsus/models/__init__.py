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

"""Object models for Nautobot FSUS."""
from nautobot_fsus.models.fsu_templates import (
    CPUTemplate,
    DiskTemplate,
    FanTemplate,
    GPUBaseboardTemplate,
    GPUTemplate,
    HBATemplate,
    MainboardTemplate,
    NICTemplate,
    OtherFSUTemplate,
    PSUTemplate,
    RAMModuleTemplate,
)
from nautobot_fsus.models.fsu_types import (
    CPUType,
    DiskType,
    FanType,
    GPUBaseboardType,
    GPUType,
    HBAType,
    MainboardType,
    NICType,
    OtherFSUType,
    PSUType,
    RAMModuleType,
)
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


__all__ = (
    "CPU",
    "CPUTemplate",
    "CPUType",
    "Disk",
    "DiskTemplate",
    "DiskType",
    "Fan",
    "FanTemplate",
    "FanType",
    "GPUBaseboard",
    "GPUBaseboardTemplate",
    "GPUBaseboardType",
    "GPU",
    "GPUTemplate",
    "GPUType",
    "HBA",
    "HBATemplate",
    "HBAType",
    "Mainboard",
    "MainboardTemplate",
    "MainboardType",
    "NIC",
    "NICTemplate",
    "NICType",
    "OtherFSU",
    "OtherFSUTemplate",
    "OtherFSUType",
    "PSU",
    "PSUTemplate",
    "PSUType",
    "RAMModule",
    "RAMModuleTemplate",
    "RAMModuleType",
)
