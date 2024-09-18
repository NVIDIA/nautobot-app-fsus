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

"""Filters and FilterSets for Nautobot FSUs app models"""
from nautobot_fsus.filters.fsu_templates import (
    CPUTemplateFilterSet,
    DiskTemplateFilterSet,
    FanTemplateFilterSet,
    GPUBaseboardTemplateFilterSet,
    GPUTemplateFilterSet,
    HBATemplateFilterSet,
    MainboardTemplateFilterSet,
    NICTemplateFilterSet,
    OtherFSUTemplateFilterSet,
    PSUTemplateFilterSet,
    RAMModuleTemplateFilterSet,
)
from nautobot_fsus.filters.fsu_types import (
    CPUTypeFilterSet,
    DiskTypeFilterSet,
    FanTypeFilterSet,
    GPUBaseboardTypeFilterSet,
    GPUTypeFilterSet,
    HBATypeFilterSet,
    MainboardTypeFilterSet,
    NICTypeFilterSet,
    OtherFSUTypeFilterSet,
    PSUTypeFilterSet,
    RAMModuleTypeFilterSet,
)
from nautobot_fsus.filters.fsus import (
    CPUFilterSet,
    DiskFilterSet,
    FanFilterSet,
    GPUBaseboardFilterSet,
    GPUFilterSet,
    HBAFilterSet,
    MainboardFilterSet,
    NICFilterSet,
    OtherFSUFilterSet,
    PSUFilterSet,
    RAMModuleFilterSet,
)

__all__ = (
    "CPUFilterSet",
    "CPUTemplateFilterSet",
    "CPUTypeFilterSet",
    "DiskFilterSet",
    "DiskTemplateFilterSet",
    "DiskTypeFilterSet",
    "FanFilterSet",
    "FanTemplateFilterSet",
    "FanTypeFilterSet",
    "GPUBaseboardFilterSet",
    "GPUBaseboardTemplateFilterSet",
    "GPUBaseboardTypeFilterSet",
    "GPUFilterSet",
    "GPUTemplateFilterSet",
    "GPUTypeFilterSet",
    "HBAFilterSet",
    "HBATemplateFilterSet",
    "HBATypeFilterSet",
    "MainboardFilterSet",
    "MainboardTemplateFilterSet",
    "MainboardTypeFilterSet",
    "NICFilterSet",
    "NICTemplateFilterSet",
    "NICTypeFilterSet",
    "OtherFSUFilterSet",
    "OtherFSUTemplateFilterSet",
    "OtherFSUTypeFilterSet",
    "PSUFilterSet",
    "PSUTemplateFilterSet",
    "PSUTypeFilterSet",
    "RAMModuleFilterSet",
    "RAMModuleTemplateFilterSet",
    "RAMModuleTypeFilterSet",
)
