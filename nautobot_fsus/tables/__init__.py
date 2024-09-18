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

"""Table definitions for the Nautobot FSUs app."""
from nautobot_fsus.tables.fsu_templates import (
    CPUTemplateTable,
    DiskTemplateTable,
    FanTemplateTable,
    GPUBaseboardTemplateTable,
    GPUTemplateTable,
    HBATemplateTable,
    MainboardTemplateTable,
    NICTemplateTable,
    OtherFSUTemplateTable,
    PSUTemplateTable,
    RAMModuleTemplateTable
)
from nautobot_fsus.tables.fsu_types import (
    CPUTypeTable,
    DiskTypeTable,
    FanTypeTable,
    GPUBaseboardTypeTable,
    GPUTypeTable,
    HBATypeTable,
    MainboardTypeTable,
    NICTypeTable,
    OtherFSUTypeTable,
    PSUTypeTable,
    RAMModuleTypeTable,
)
from nautobot_fsus.tables.fsus import (
    CPUImportTable,
    CPUTable,
    DiskImportTable,
    DiskTable,
    FanImportTable,
    FanTable,
    GPUBaseboardImportTable,
    GPUBaseboardTable,
    GPUImportTable,
    GPUTable,
    HBAImportTable,
    HBATable,
    MainboardImportTable,
    MainboardTable,
    NICImportTable,
    NICTable,
    OtherFSUImportTable,
    OtherFSUTable,
    PSUImportTable,
    PSUTable,
    RAMModuleImportTable,
    RAMModuleTable,
)


__all__ = (
    "CPUImportTable",
    "CPUTable",
    "CPUTemplateTable",
    "CPUTypeTable",
    "DiskImportTable",
    "DiskTable",
    "DiskTemplateTable",
    "DiskTypeTable",
    "FanImportTable",
    "FanTable",
    "FanTemplateTable",
    "FanTypeTable",
    "GPUBaseboardImportTable",
    "GPUBaseboardTable",
    "GPUBaseboardTemplateTable",
    "GPUBaseboardTypeTable",
    "GPUImportTable",
    "GPUTable",
    "GPUTemplateTable",
    "GPUTypeTable",
    "HBAImportTable",
    "HBATable",
    "HBATemplateTable",
    "HBATypeTable",
    "MainboardImportTable",
    "MainboardTable",
    "MainboardTemplateTable",
    "MainboardTypeTable",
    "NICImportTable",
    "NICTable",
    "NICTemplateTable",
    "NICTypeTable",
    "OtherFSUImportTable",
    "OtherFSUTable",
    "OtherFSUTemplateTable",
    "OtherFSUTypeTable",
    "PSUImportTable",
    "PSUTable",
    "PSUTemplateTable",
    "PSUTypeTable",
    "RAMModuleImportTable",
    "RAMModuleTable",
    "RAMModuleTemplateTable",
    "RAMModuleTypeTable",
)
