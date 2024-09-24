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

"""Test cases for Nautobot FSUs app models."""
from time import sleep
from typing import Any, Type

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from nautobot.dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer, Site
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot.extras.models import CustomField, Status

from nautobot_fsus.models import FanType, OtherFSUType
from nautobot_fsus.models.mixins import FSUModel, FSUTemplateModel, FSUTypeModel, PCIFSUModel


class NautobotFSUModelTestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for testing FSU models."""

    class FSUTestCase(TestCase):
        """Common test case for FSU models."""

        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]
        parent_model: Type[FSUModel]
        parent_model_type: Type[FSUTypeModel]
        parent_field: str | None = None
        child_model: Type[FSUModel]
        child_model_type: Type[FSUTypeModel]
        child_field: str | None = None

        def setUp(self) -> None:
            """Set up objects for the tests."""
            self.manufacturer = Manufacturer.objects.first()
            self.device = Device.objects.first()
            self.location = Location.objects.first()
            self.status = Status.objects.get_for_model(self.model).first()

            self.fsu_type = self.type_model.objects.create(
                manufacturer=self.manufacturer,
                name=f"Test {self.model._meta.verbose_name}",
                part_number="0001",
            )

        def test_fsu_creation(self):
            """Ensure an FSU instance can be created."""
            instance = self.model(
                fsu_type=self.fsu_type,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )

            self.assertIsNone(instance.parent)
            with self.assertRaises(ValidationError):
                instance.full_clean()

            instance.device = self.device
            instance.save()

            self.assertEqual(str(instance), instance.name)
            self.assertEqual(instance.parent, instance.device)

            object_change = instance.to_objectchange("create")
            self.assertEqual(
                object_change.changed_object_type.model_class(),
                instance._meta.model,
            )
            self.assertEqual(object_change.related_object_id, instance.parent.id)

        def test_export_fsu(self):
            """Test exporting an FSU instance to CSV."""
            instance = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )
            if isinstance(instance, PCIFSUModel):
                instance.pci_slot_id = "00000000:07:00.0"
            instance.save()

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), len(instance.csv_headers))
            for index, value in enumerate(instance.csv_headers):
                match = str(getattr(instance, value)) if getattr(instance, value) is not None else ""
                self.assertEqual(str(csv[index]), match)

        def test_move_to_device(self):
            """Ensure when a device is set on an FSU instance, the storage location is cleared."""
            instance = self.model(
                fsu_type=self.fsu_type,
                location=self.location,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )
            instance.save()

            self.assertEqual(instance.parent, self.location)
            self.assertIsNone(instance.device)

            instance.device = self.device
            instance.save()

            self.assertIsNone(instance.location)
            self.assertEqual(instance.parent, self.device)

        def test_duplicate_names(self):
            """Verify unique name constraints for FSUs in the same device or location."""
            instance1 = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )
            instance1.save()

            instance2 = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=instance1.name,
                status=self.status,
            )

            with self.assertRaises(ValidationError):
                instance2.full_clean()

            instance1.device = Device.objects.last()
            instance1.save()
            instance2.full_clean()

            instance1.device = None
            instance1.location = self.location
            instance1.save()

            instance2.device = None
            instance2.location = self.location
            with self.assertRaises(ValidationError):
                instance2.full_clean()

            instance1.location = Location.objects.last()
            instance1.save()
            instance2.full_clean()

        def test_fsu_incorrect_type(self):
            """Verify validation of the correct FSU type on FSU creation."""
            # if self.model._meta.model_name == "otherfsu":
            if self.model._meta.model_name == "otherfsu":
                bad_type = FanType(
                    manufacturer=self.manufacturer,
                    name="Bad FSU Type",
                    part_number="0002",
                )
            else:
                bad_type = OtherFSUType(
                    manufacturer=self.manufacturer,
                    name="Bad FSU Type",
                    part_number="0002",
                )
            bad_type.save()

            with self.assertRaises(ValueError):
                _ = self.model(
                    fsu_type=bad_type,
                    device=self.device,
                    name=f"test_{self.model._meta.model_name}",
                    status=self.status,
                )

        def test_parent_fsu(self):
            """Test assigning a parent FSU to a child instance."""
            if (not hasattr(self, "parent_model") or not hasattr(self, "parent_model_type")
                    or self.parent_field is None):
                self.skipTest("Parent FSU model/type/field not set.")

            parent_type = self.parent_model_type(
                manufacturer=self.manufacturer,
                name=self.parent_field,
                part_number="x1",
            )
            parent_type.save()

            parent_instance = self.parent_model(
                fsu_type=parent_type,
                device=self.device,
                name=f"test_{self.parent_model._meta.model_name}",
                status=self.status,
            )
            parent_instance.save()

            instance = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )
            setattr(instance, self.parent_field, parent_instance)
            instance.validated_save()

        def test_parent_bad_device(self):
            """Test assigning a parent FSU on a different device to a child instance."""
            if (not hasattr(self, "parent_model") or not hasattr(self, "parent_model_type")
                    or self.parent_field is None):
                self.skipTest("Parent FSU model/type/field not set.")

            parent_type = self.parent_model_type(
                manufacturer=self.manufacturer,
                name=self.parent_field,
                part_number="x1",
            )
            parent_type.save()

            parent_instance = self.parent_model(
                fsu_type=parent_type,
                location=self.location,
                name=f"test_{self.parent_model._meta.model_name}",
                status=self.status,
            )
            parent_instance.save()

            instance = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=f"test_{self.model._meta.model_name}",
                status=self.status,
            )
            setattr(instance, self.parent_field, parent_instance)

            with self.subTest("no_parent_device"):
                with self.assertRaises(ValidationError) as context:
                    instance.full_clean()
                error = context.exception
                self.assertEqual(
                    error.messages[0],
                    "Parent FSU must be assigned to a device in order to add child FSUs",
                )

            with self.subTest("bad_parent_device"):
                parent_instance.location = None
                parent_instance.device = Device.objects.last()
                parent_instance.save()
                with self.assertRaises(ValidationError) as context:
                    instance.full_clean()
                error = context.exception
                self.assertEqual(
                    error.messages[0],
                    f"{instance._meta.verbose_name} {instance.name} has a different parent "
                    f"device ({instance.device.name}) than that of its parent FSU "
                    f"({parent_instance.device.name})"
                )

        def test_child_fsu(self):
            """Test assigning a child FSU to a parent instance."""
            if (not hasattr(self, "child_model") or not hasattr(self, "child_model_type")
                    or self.child_field is None):
                self.skipTest("Child FSU model/type/field not set.")

            child_type = self.child_model_type(
                manufacturer=self.manufacturer,
                name=self.child_field,
                part_number="x1",
            )
            child_type.save()

            child_instance = self.child_model(
                fsu_type=child_type,
                device=self.device,
                name=f"test_child_{self.child_model._meta.model_name}",
                status=self.status,
            )
            child_instance.save()

            instance = self.model(
                fsu_type=self.fsu_type,
                device=self.device,
                name=f"test_parent_{self.model._meta.model_name}",
                status=self.status,
            )
            instance.validated_save()
            getattr(instance, self.child_field).set([child_instance])

            self.assertEqual(
                getattr(child_instance, f"parent_{self.model._meta.model_name}"),
                instance
            )

    class FSUTemplateTestCase(TestCase):
        """Common test cases for FSUTemplates."""

        template_model: Type[FSUTemplateModel]
        type_model: Type[FSUTypeModel]
        target_model: Type[FSUModel]

        def setUp(self):
            """Set up objects for the tests."""
            self.manufacturers = [Manufacturer.objects.first(), Manufacturer.objects.last()]

            self.device_type = DeviceType.objects.create(
                manufacturer=self.manufacturers[0],
                model="Test Device Type",
                slug="test_device_type",
            )

            self.fsu_type = self.type_model.objects.create(
                manufacturer=self.manufacturers[0],
                name=f"Test {self.target_model._meta.verbose_name}",
                part_number="0001",
            )

        def test_template_change_log(self):
            """Verify template change log entry."""
            template = self.template_model.objects.create(
                device_type=self.device_type,
                name="test_template",
                fsu_type=self.fsu_type,
            )

            object_change = template.to_objectchange("create")
            self.assertEqual(object_change.changed_object_type.model_class(), template._meta.model)
            self.assertEqual(object_change.changed_object_id, template.id)
            self.assertEqual(
                object_change.related_object_type.model_class(),
                template.device_type._meta.model
            )
            self.assertEqual(object_change.related_object_id, template.device_type.id)

        def test_create_and_assign_templates(self):
            """Test creating a template instance and assigning it to a DeviceType."""
            template = self.template_model.objects.create(
                device_type=self.device_type,
                name=f"test_{self.target_model._meta.model_name}_0",
                fsu_type=self.fsu_type,
            )

            self.assertEqual(
                getattr(self.device_type, f"{self.template_model._meta.model_name}s").count(),
                1
            )
            self.assertEqual(
                getattr(self.device_type, f"{self.template_model._meta.model_name}s").first().name,
                template.name
            )

        def test_instantiate_target_fsu(self):
            """Test that the target FSU is present on a new Device."""
            custom_field = CustomField.objects.create(
                type=CustomFieldTypeChoices.TYPE_TEXT,
                name="cf_field_1",
                default="value_1",
            )
            custom_field.content_types.set([ContentType.objects.get_for_model(self.target_model)])

            template = self.template_model.objects.create(
                device_type=self.device_type,
                name=f"test_{self.target_model._meta.model_name}_0",
                fsu_type=self.fsu_type,
            )

            device = Device.objects.create(
                device_type=self.device_type,
                device_role=DeviceRole.objects.first(),
                status=Status.objects.get_for_model(Device).first(),
                name="Device X",
                site=Site.objects.first(),
            )

            # Pause for the signal
            sleep(1)

            instance = getattr(device, f"{self.target_model._meta.model_name}s").first()
            self.assertIsNotNone(instance)
            self.assertEqual(instance.name, template.name)
            self.assertEqual(instance.cf["cf_field_1"], custom_field.default)

    class FSUTypeTestCase(TestCase):
        """Common test cases for FSUType models."""

        type_model: Type[FSUTypeModel]
        model_fields: dict[str, Any] = {}

        def setUp(self) -> None:
            """Set up objects for the tests."""
            self.manufacturer = Manufacturer.objects.first()

        def test_export_fsu_type(self):
            """Test exporting an FSU type instance to CSV."""
            instance = self.type_model(
                manufacturer=self.manufacturer,
                name=f"Test {self.type_model._meta.verbose_name}",
                part_number="0001",
            )
            for key, value in self.model_fields.items():
                setattr(instance, key, value)

            csv = instance.to_csv()
            self.assertIsInstance(csv, tuple)
            self.assertEqual(len(csv), len(instance.csv_headers))
            self.assertEqual(csv[1], instance.name)

        def test_duplicate_part_number(self):
            """Verify unique part number constraint."""
            _ = self.type_model.objects.create(
                manufacturer=self.manufacturer,
                name=f"Test {self.type_model._meta.verbose_name} 1",
                part_number="0001"
            )

            instance = self.type_model(
                manufacturer=self.manufacturer,
                name=f"Test {self.type_model._meta.verbose_name} 2",
                part_number="0001"
            )

            with self.assertRaises(ValidationError):
                instance.full_clean()

            instance.manufacturer = Manufacturer.objects.last()
            instance.full_clean()
