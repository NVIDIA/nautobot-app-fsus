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

"""Tests for FSUTemplate model views defined in the Nautobot FSUs app."""
from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings
from django.urls import reverse
from nautobot.dcim.models import DeviceType, Manufacturer
from nautobot.users.models import ObjectPermission
from nautobot.utilities.testing import extract_page_body, post_data, ViewTestCases

from nautobot_fsus import models
from nautobot_fsus.models.mixins import FSUTemplateModel, FSUTypeModel


class FSUTemplateViewTestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for testing FSUTemplate model views."""

    class FSUTemplateModelViewTestCase(
        ViewTestCases.GetObjectViewTestCase,
        ViewTestCases.GetObjectChangelogViewTestCase,
        ViewTestCases.GetObjectNotesViewTestCase,
        ViewTestCases.CreateMultipleObjectsViewTestCase,
        ViewTestCases.EditObjectViewTestCase,
        ViewTestCases.DeleteObjectViewTestCase,
        ViewTestCases.ListObjectsViewTestCase,
    ):
        """Common tests for FSUTemplate model views."""

        model: Type[FSUTemplateModel]
        type_model: Type[FSUTypeModel]

        @classmethod
        def setUpTestData(cls):
            """Set up initial test data."""
            object_name = cls.model._meta.object_name.replace("Template", "")

            manufacturers = [
                Manufacturer.objects.create(
                    name="Device Manufacturer",
                    slug="device-manufacturer",
                ),
                Manufacturer.objects.create(
                    name="FSU Manufacturer",
                    slug="fsu-manufacturer"
                )
            ]

            device_types = [
                DeviceType.objects.create(
                    manufacturer=manufacturers[0],
                    model="Test Device Type 1",
                    slug="test-device-type-1",
                ),
                DeviceType.objects.create(
                    manufacturer=manufacturers[0],
                    model="Test Device Type 2",
                    slug="test-device-type-2",
                ),
            ]

            fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=manufacturers[1],
                    name=f"Test {object_name} 1",
                    part_number="0001",
                ),
                cls.type_model.objects.create(
                    manufacturer=manufacturers[1],
                    name=f"Test {object_name} 2",
                    part_number="0002",
                ),
            ]

            for i in range(1, 4):
                cls.model.objects.create(
                    device_type=device_types[0],
                    fsu_type=fsu_types[0],
                    name=f"test_{object_name.lower()}_{i}",
                )

            cls.form_data = {
                "device_type": DeviceType.objects.last().pk,
                "fsu_type": cls.type_model.objects.last().pk,
                "name": f"test_{object_name.lower()}_X",
            }

            cls.bulk_create_data = {
                "device_type": device_types[1].pk,
                "fsu_type": fsu_types[1].pk,
                "name_pattern": f"test_{object_name.lower()}_[4-6]",
            }

            cls.bulk_edit_data = {"fsu_type": fsu_types[1].pk}

        @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
        def test_create_object_with_addanother(self):
            """Test that setting `_addanother` redirects back to the form."""
            self.form_data = self.form_data.copy()
            self.form_data["name_pattern"] = self.form_data["name"]
            self.form_data.pop("name")
            self.form_data["_addanother"] = ""

            initial_count = self._get_queryset().count()
            obj_perm = ObjectPermission(name="Test permission", actions=["add"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ContentType.objects.get_for_model(self.model))

            request = {
                "path": self._get_url("add"),
                "data": post_data(self.form_data),
            }
            response = self.client.post(**request)
            self.assertHttpStatus(response, 302)
            self.assertEqual(initial_count + 1, self._get_queryset().count())
            self.assertEqual(
                response.url,
                reverse(f"plugins:nautobot_fsus:{self.model._meta.model_name}_add"),
            )

        @override_settings(EXEMPT_VIEW_PERMISSIONS=[])
        def test_create_object_with_bad_data(self):
            """Test that errors are set and returned on the form for bad data."""
            self.form_data = self.form_data.copy()
            self.form_data.pop("name")

            obj_perm = ObjectPermission(name="Test permission", actions=["add"])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ContentType.objects.get_for_model(self.model))

            self.form_data["name_pattern"] = f"test-{'X' * 128}"
            response = self.client.post(path=self._get_url("add"), data=post_data(self.form_data))
            response_body = extract_page_body(response.content.decode(response.charset))
            self.assertIn("FORM-ERROR name_pattern", response_body)

            if hasattr(self.model, "pci_slot_id"):
                self.form_data["name_pattern"] = "test-X"
                self.form_data["pci_slot_id_pattern"] = f"Test {'X' * 128}"

                response = self.client.post(path=self._get_url("add"), data=post_data(self.form_data))
                response_body = extract_page_body(response.content.decode(response.charset))
                self.assertIn("FORM-ERROR pci_slot_id_pattern", response_body)

            if hasattr(self.model, "slot_id"):
                self.form_data["name_pattern"] = "test-X"
                self.form_data["slot_id_pattern"] = f"Test {'X' * 32}"

                response = self.client.post(path=self._get_url("add"),
                                            data=post_data(self.form_data))
                response_body = extract_page_body(response.content.decode(response.charset))
                self.assertIn("FORM-ERROR slot_id_pattern", response_body)


class CPUTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for CPUTemplate model views."""

    model = models.CPUTemplate
    type_model = models.CPUType


class DiskTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for DiskTemplate model views."""

    model = models.DiskTemplate
    type_model = models.DiskType


class FanTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for FanTemplate model views."""

    model = models.FanTemplate
    type_model = models.FanType


class GPUTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for GPUTemplate model views."""

    model = models.GPUTemplate
    type_model = models.GPUType


class GPUBaseboardTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for GPUBaseboardTemplate model views."""

    model = models.GPUBaseboardTemplate
    type_model = models.GPUBaseboardType


class HBATemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for HBATemplate model views."""

    model = models.HBATemplate
    type_model = models.HBAType


class MainboardTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for MainboardTemplate model views."""

    model = models.MainboardTemplate
    type_model = models.MainboardType


class NICTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for NICTemplate model views."""

    model = models.NICTemplate
    type_model = models.NICType


class OtherFSUTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for OtherFSUTemplate model views."""

    model = models.OtherFSUTemplate
    type_model = models.OtherFSUType


class PSUTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for PSUTemplate model views."""

    model = models.PSUTemplate
    type_model = models.PSUType


class RAMModuleTemplateViewTestCase(FSUTemplateViewTestCases.FSUTemplateModelViewTestCase):
    """Tests for RAMModuleTemplate model views."""

    model = models.RAMModuleTemplate
    type_model = models.RAMModuleType
