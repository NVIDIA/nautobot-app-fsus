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

"""Tests for FSU Type models defined by the Nautobot FSUS app."""
from nautobot_fsus import models
from nautobot_fsus.utilities.testing import NautobotFSUModelTestCases


class CPUTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the CPUType model."""

    type_model = models.CPUType
    model_fields = {"architecture": "arm"}


class DiskTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the DiskType model."""

    type_model = models.DiskType
    model_fields = {"architecture": "arm"}


class FanTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the FanType model."""

    type_model = models.FanType
    model_fields = {"architecture": "arm"}


class GPUTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the GPUType model."""

    type_model = models.GPUType
    model_fields = {"architecture": "arm"}


class GPUBaseboardTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the GPUBaseboardType model."""

    type_model = models.GPUBaseboardType
    model_fields = {"architecture": "arm"}


class HBATypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the HBAType model."""

    type_model = models.HBAType
    model_fields = {"architecture": "arm"}


class MainboardTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the MainboardType model."""

    type_model = models.MainboardType
    model_fields = {"architecture": "arm"}


class NICTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the NICType model."""

    type_model = models.NICType
    model_fields = {"architecture": "arm"}


class OtherFSUTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the OtherFSUType model."""

    type_model = models.OtherFSUType
    model_fields = {"architecture": "arm"}


class PSUTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the PSUType model."""

    type_model = models.PSUType
    model_fields = {"architecture": "arm"}


class RAMModuleTypeTestCase(NautobotFSUModelTestCases.FSUTypeTestCase):
    """Tests for the RAMModuleType model."""

    type_model = models.RAMModuleType
    model_fields = {"architecture": "arm"}
