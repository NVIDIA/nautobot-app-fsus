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

"""Tests for FSUType model views defined in the Nautobot FSUs app."""
from typing import Type

from nautobot.dcim.models import Manufacturer
from nautobot.utilities.testing import ViewTestCases

from nautobot_fsus import models
from nautobot_fsus.models.mixins import FSUTypeModel


class FSUTypeViewTestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for testing FSUType model views."""

    class FSUTypeModelViewTestCase(ViewTestCases.PrimaryObjectViewTestCase,):
        """Common tests for FSUType model views."""

        model: Type[FSUTypeModel]

        @classmethod
        def setUpTestData(cls):
            """Set up initial test data."""
            manufacturers = Manufacturer.objects.all()

            cls.form_data = {
                "manufacturer": manufacturers[1].pk,
                "name": f"{cls.model._meta.verbose_name} X",
                "part_number": "X23",
            }

            new_mfgr = Manufacturer.objects.create(name="Test Manufacturer")
            cls.bulk_edit_data = {"manufacturer": new_mfgr.pk}

            cls.csv_data = (
                "manufacturer,name,part_number",
                f"{manufacturers[1].name},{cls.model._meta.verbose_name} 7,0007",
                f"{manufacturers[1].name},{cls.model._meta.verbose_name} 8,0008",
                f"{manufacturers[1].name},{cls.model._meta.verbose_name} 9,0009",
            )


class CPUTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for CPUType model views."""

    model = models.CPUType

    @classmethod
    def setUpTestData(cls):
        """Set CPUType-specific options."""
        super().setUpTestData()

        cls.form_data.update({
            "architecture": "arm",
            "cpu_speed": 2.5,
            "cores": 8,
        })
        cls.bulk_edit_data.update({
            "architecture": "x86",
            "cpu_speed": 1.5,
            "cores": 16,
        })

        cls.csv_data = (
            "manufacturer,name,part_number,architecture",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 7,0007,x86",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 8,0008,x86",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 9,0009,arm",
        )


class DiskTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for DiskType model views."""

    model = models.DiskType

    @classmethod
    def setUpTestData(cls):
        """Set DiskType-specific options."""
        super().setUpTestData()

        cls.form_data["disk_type"] = "SSD"

        cls.csv_data = (
            "manufacturer,name,part_number,disk_type",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 7,0007,SSD",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 8,0008,NVME",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 9,0009,NVME",
        )


class FanTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for FanType model views."""

    model = models.FanType


class GPUTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for GPUType model views."""

    model = models.GPUType


class GPUBaseboardTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for GPUBaseboardType model views."""

    model = models.GPUBaseboardType


class HBATypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for HBAType model views."""

    model = models.HBAType


class MainboardTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for MainboardType model views."""

    model = models.MainboardType


class NICTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for NICType model views."""

    model = models.NICType


class OtherFSUTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for OtherFSUType model views."""

    model = models.OtherFSUType


class PSUTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for PSUType model views."""

    model = models.PSUType

    @classmethod
    def setUpTestData(cls):
        """Set PSUType-specific options."""
        super().setUpTestData()

        cls.bulk_edit_data["feed_type"] = "dc"

        cls.csv_data = (
            "manufacturer,name,part_number,feed_type",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 7,0007,dc",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 8,0008,dc",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 9,0009,ac",
        )


class RAMModuleTypeViewTestCase(FSUTypeViewTestCases.FSUTypeModelViewTestCase):
    """Tests for RAMModuleType model views."""

    model = models.RAMModuleType

    @classmethod
    def setUpTestData(cls):
        """Set RAMModuleType-specific options."""
        super().setUpTestData()

        cls.form_data.update({"module_type": "u", "technology": "ddr5", "quantity": 1})

        cls.csv_data = (
            "manufacturer,name,part_number,module_type,technology,quantity",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 7,0007,u,ddr5,1",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 8,0008,u,ddr5,1",
            f"{Manufacturer.objects.last().name},{cls.model._meta.verbose_name} 9,0009,ue,ddr5,2",
        )
