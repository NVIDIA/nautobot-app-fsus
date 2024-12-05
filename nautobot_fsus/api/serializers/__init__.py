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

"""API serializers for Nautobot FSUs app models."""

from nautobot_fsus.api.serializers.fsu_templates import (
    CPUTemplateSerializer,
    DiskTemplateSerializer,
    FanTemplateSerializer,
    GPUBaseboardTemplateSerializer,
    GPUTemplateSerializer,
    HBATemplateSerializer,
    MainboardTemplateSerializer,
    NICTemplateSerializer,
    OtherFSUTemplateSerializer,
    PSUTemplateSerializer,
    RAMModuleTemplateSerializer,
)
from nautobot_fsus.api.serializers.fsu_types import (
    CPUTypeSerializer,
    DiskTypeSerializer,
    FanTypeSerializer,
    GPUBaseboardTypeSerializer,
    GPUTypeSerializer,
    HBATypeSerializer,
    MainboardTypeSerializer,
    NICTypeSerializer,
    OtherFSUTypeSerializer,
    PSUTypeSerializer,
    RAMModuleTypeSerializer,
)
from nautobot_fsus.api.serializers.fsus import (
    CPUSerializer,
    DiskSerializer,
    FanSerializer,
    GPUBaseboardSerializer,
    GPUSerializer,
    HBASerializer,
    MainboardSerializer,
    NICSerializer,
    OtherFSUSerializer,
    PSUSerializer,
    RAMModuleSerializer,
)

__all__ = (
    "CPUSerializer",
    "CPUTemplateSerializer",
    "CPUTypeSerializer",
    "DiskSerializer",
    "DiskTemplateSerializer",
    "DiskTypeSerializer",
    "FanSerializer",
    "FanTemplateSerializer",
    "FanTypeSerializer",
    "GPUBaseboardSerializer",
    "GPUBaseboardTemplateSerializer",
    "GPUBaseboardTypeSerializer",
    "GPUSerializer",
    "GPUTemplateSerializer",
    "GPUTypeSerializer",
    "HBASerializer",
    "HBATemplateSerializer",
    "HBATypeSerializer",
    "MainboardSerializer",
    "MainboardTemplateSerializer",
    "MainboardTypeSerializer",
    "NICSerializer",
    "NICTemplateSerializer",
    "NICTypeSerializer",
    "OtherFSUSerializer",
    "OtherFSUTemplateSerializer",
    "OtherFSUTypeSerializer",
    "PSUSerializer",
    "PSUTemplateSerializer",
    "PSUTypeSerializer",
    "RAMModuleSerializer",
    "RAMModuleTemplateSerializer",
    "RAMModuleTypeSerializer",
)
