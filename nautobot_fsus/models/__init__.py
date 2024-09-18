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
    "CPUType",
    "Disk",
    "DiskType",
    "Fan",
    "FanType",
    "GPUBaseboard",
    "GPUBaseboardType",
    "GPU",
    "GPUType",
    "HBA",
    "HBAType",
    "Mainboard",
    "MainboardType",
    "NIC",
    "NICType",
    "OtherFSU",
    "OtherFSUType",
    "PSU",
    "PSUType",
    "RAMModule",
    "RAMModuleType",
)
