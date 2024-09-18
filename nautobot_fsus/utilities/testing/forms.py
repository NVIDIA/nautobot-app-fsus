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

"""Test cases for forms."""
from typing import Type

from nautobot.dcim.models import Device, DeviceType, Manufacturer
from nautobot.extras.models import Status
from nautobot.extras.forms import NautobotBulkEditForm, NautobotFilterForm
from nautobot.utilities.testing import TestCase

from nautobot_fsus.forms.mixins import (
    BaseFSUCSVForm,
    FSUModelBulkEditForm,
    FSUModelFilterForm,
    FSUModelForm,
    FSUTemplateCreateForm,
    FSUTemplateModelForm,
    FSUTypeModelForm,
)
from nautobot_fsus.models.mixins import FSUModel, FSUTemplateModel, FSUTypeModel


class FSUFormTestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for Nautobot FSU form tests."""

    class FSUModelFormTestCase(TestCase):
        """Common tests for FSU forms."""

        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]
        form_model: Type[FSUModelForm]
        bulk_form_model: Type[FSUModelBulkEditForm]
        filter_form_model: Type[FSUModelFilterForm]
        csv_form_model: Type[BaseFSUCSVForm]

        @classmethod
        def setUpTestData(cls):
            """Create initial test data."""
            cls.fsu_type = cls.type_model.objects.create(
                name=f"Test {cls.type_model._meta.object_name}",
                manufacturer=Manufacturer.objects.first(),
                part_number="x001",
            )

        def test_new_fsu(self):
            """The create FSU form."""
            form = self.form_model(
                data={
                    "fsu_type": self.fsu_type,
                    "device": Device.objects.first(),
                    "name": f"{self.model._meta.model_name}_0",
                    "serial_number": "a001",
                    "firmware_version": "1.0",
                    "driver_name": "test_driver",
                    "driver_version": "1.0",
                    "status": Status.objects.get_for_model(self.model).first(),
                }
            )
            self.assertTrue(form.is_valid())
            self.assertTrue(form.save())

        def test_edit_fsu(self):
            """The update FSU form."""
            fsu = self.model.objects.create(
                fsu_type=self.fsu_type,
                device=Device.objects.first(),
                name=f"{self.model._meta.model_name}_0",
            )

            form = self.form_model(instance=fsu)
            self.assertEqual(form["name"].initial, fsu.name)

    class FSUTemplateFormTestCase(TestCase):
        """Tests for FSU template forms."""
        model: Type[FSUTemplateModel]
        type_model: Type[FSUTypeModel]
        form_model: Type[FSUTemplateModelForm]
        bulk_form_model: Type[NautobotBulkEditForm]
        create_form_model: Type[FSUTemplateCreateForm]

        @classmethod
        def setUpTestData(cls):
            """Create initial data for the tests."""
            cls.fsu_type = cls.type_model.objects.create(
                manufacturer=Manufacturer.objects.first(),
                name="TestGPU",
                part_number="x001",
            )

        def test_new_fsutemplate(self):
            """Test adding a new FSU template."""
            instance_type = self.model._meta.object_name.replace("Template", "")
            form = self.form_model(
                data={
                    "fsu_type": self.fsu_type,
                    "device_type": DeviceType.objects.first(),
                    "name": f"{ instance_type.lower() }_0",
                    "description": f"Test { instance_type }",
                }
            )
            self.assertTrue(form.is_valid())
            self.assertTrue(form.save())

        def test_edit_fsutemplate(self):
            """Test creating the form with an existing FSU template."""
            instance_type = self.model._meta.object_name.replace("Template", "")
            fsu_template = self.model.objects.create(
                fsu_type=self.fsu_type,
                device_type=DeviceType.objects.first(),
                name=f"test_{ instance_type }",
            )

            form = self.form_model(instance=fsu_template)
            if hasattr(self.model, "pci_slot_id"):
                self.assertIn("pci_slot_id", form.fields)
            if hasattr(self.model, "redundant"):
                self.assertIn("redundant", form.fields)
            self.assertEqual(form["name"].initial, fsu_template.name)

        def test_fsutemplate_bulk_create_form(self):
            """Test creating the FSU template bulk create form."""
            form = self.create_form_model()
            self.assertIn("name_pattern", form.fields)

        def test_fsutemplate_bulk_edit_form(self):
            """Test creating the FSU template bulk editing form."""
            form = self.bulk_form_model(self.model)
            self.assertIn("fsu_type", form.fields)
            self.assertNotIn("device_type", form.fields)

    class FSUTypeFormTestCase(TestCase):
        """Common tests for FSU Type forms."""
        type_model: Type[FSUTypeModel]
        form_model: Type[FSUTypeModelForm]
        bulk_form_model: Type[NautobotBulkEditForm]
        filter_form_model: Type[NautobotFilterForm]

        @classmethod
        def setUpTestData(cls):
            """Create initial data for the tests."""
            cls.instance_model = cls.type_model._meta.object_name.replace('Type', '')

        def test_new_fsu_type(self):
            """Test adding a new FSU type."""
            form = self.form_model(
                data={
                    "manufacturer": Manufacturer.objects.first(),
                    "name": f"Test { self.instance_model }",
                    "part_number": "X0001Z",
                }
            )
            self.assertTrue(form.is_valid())
            self.assertTrue(form.save())

        def test_edit_fsu_type(self):
            """Test creating the form with an existing FSU type."""
            fsu_type = self.type_model.objects.create(
                manufacturer=Manufacturer.objects.first(),
                name=f"Test { self.instance_model }",
                part_number="X0001Z",
            )

            form = self.form_model(instance=fsu_type)
            self.assertEqual(form["name"].initial, fsu_type.name)
