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

"""Test cases the api."""
from typing import Type

from django.urls import reverse
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer
from nautobot.dcim.models.device_components import ComponentModel
from nautobot.extras.models import Status
from nautobot.utilities.testing.api import APIViewTestCases
from rest_framework import status

from nautobot_fsus.models.mixins import FSUModel, FSUTemplateModel, FSUTypeModel


class FSUAPITestCases:  # pylint: disable=too-few-public-methods
    """Wrapper class for testing FSU API endpoints."""

    class FSUAPIViewTestCase(APIViewTestCases.APIViewTestCase):
        """Common test case for FSU APIs."""
        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]

        brief_fields = ["display", "id", "name", "url"]
        fsus: list[FSUModel]
        validation_excluded_fields = ["status"]
        bulk_update_data = {"firmware_version": "2.0"}
        choices_fields = ["status"]

        @classmethod
        def setUpTestData(cls):
            """Load initial data for the tests."""
            model_name = cls.model._meta.model_name

            cls.fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test {cls.model._meta.verbose_name}",
                    part_number="0001",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.last(),
                    name=f"Another {cls.model._meta.verbose_name}",
                    part_number="0001",
                ),
            ]

            devices = [Device.objects.first(), Device.objects.last()]
            location = Location.objects.first()
            statuses = {
                "device": Status.objects.get(name="Active"),
                "location": Status.objects.get(name="Available"),
            }

            cls.fsus = [
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
                    device=devices[0],
                    name=f"test_{model_name}_0",
                    serial_number="a0001",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["device"],
                    description=f"First test {cls.model._meta.verbose_name}",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[1],
                    device=devices[0],
                    name=f"test_{model_name}_1",
                    serial_number="a0002",
                    firmware_version="1.1",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["device"],
                    description=f"Second test {cls.model._meta.verbose_name}",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
                    location=location,
                    name=f"test_{model_name}_2",
                    serial_number="b0003",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["location"],
                    description=f"Third test {cls.model._meta.verbose_name}",
                ),
            ]

            cls.create_data = [
                {
                    "fsu_type": cls.fsu_types[0].pk,
                    "device": devices[1].pk,
                    "location": None,
                    "name": f"test_{model_name}_3",
                    "serial_number": "c0001",
                    "firmware_version": "1.0",
                    "status": "active",
                },
                {
                    "fsu_type": cls.fsu_types[0].pk,
                    "device": devices[1].pk,
                    "location": None,
                    "name": f"test_{model_name}_4",
                    "serial_number": "c0002",
                    "firmware_version": "1.0",
                    "status": "active",
                },
                {
                    "fsu_type": cls.fsu_types[1].pk,
                    "device": None,
                    "location": location.pk,
                    "name": f"test_{model_name}_5",
                    "serial_number": "d0001",
                    "firmware_version": "1.0",
                    "status": "available",
                },
            ]

        def test_unique_name_per_parent_constraint(self):
            """Test that creating an FSU with a duplicate name fails."""
            fsu = self.model.objects.get(name=self.fsus[0].name)
            model = fsu._meta.model_name
            data = {
                "fsu_type": fsu.fsu_type.pk,
                "device": fsu.device.pk,
                "name": fsu.name,
            }

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

        def test_create_fsu_with_device_and_storage_location(self):
            """Test that creating an FSU with both a device and storage location fails."""
            model = self.model._meta.model_name
            data = self.create_data[2]
            data["device"] = Device.objects.first().pk

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertEqual(
                "FSUs must be assigned to either a Device or a Storage location, but not both",
                str(response.data["non_field_errors"][0])
            )

    class ParentFSUAPIViewTestCase(FSUAPIViewTestCase):
        """Additional tests for a parent FSU."""
        child_model: Type[FSUModel]
        child_type: Type[FSUTypeModel]
        child_field: str

        @classmethod
        def setUpTestData(cls):
            """Additional setup for a parent FSU's tests."""
            super().setUpTestData()

            statuses = {
                "device": Status.objects.get(name="Active"),
                "location": Status.objects.get(name="Available"),
            }

            cls.child_fsu_type = cls.child_type.objects.create(
                manufacturer=Manufacturer.objects.first(),
                name=f"Test {cls.child_type._meta.verbose_name}",
                part_number="0001",
            )

            cls.children = [
                cls.child_model.objects.create(
                    fsu_type=cls.child_fsu_type,
                    device=Device.objects.first(),
                    name=f"test_{cls.child_model._meta.model_name}_0",
                    serial_number="a0001",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["device"],
                    description=f"First test {cls.child_model._meta.verbose_name}",
                ),
                cls.child_model.objects.create(
                    fsu_type=cls.child_fsu_type,
                    device=Device.objects.last(),
                    name=f"test_{cls.child_model._meta.model_name}_1",
                    serial_number="a0002",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    status=statuses["device"],
                    description=f"Second test {cls.child_model._meta.verbose_name}",
                ),
            ]

        def test_create_parent_with_child_in_wrong_device(self):
            """Test that creating a parent FSU with a child in a different device fails."""
            model = self.model._meta.model_name
            data = self.create_data[0]
            data[self.child_field] = [str(x.pk) for x in self.children]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0]
            self.assertEqual(
                f"{self.child_model._meta.verbose_name} {self.children[0].name} has a different "
                f"parent device (Device 1-1) than that of its parent FSU (Device 5-2)",
                str(error_message)
            )

        def test_add_parent_with_children(self):
            """Test creating a parent FSU with children."""
            model = self.model._meta.model_name
            data = self.create_data[0]
            data[self.child_field] = [self.children[1].pk]

            initial_count = self._get_queryset().count()
            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_201_CREATED)
            self.assertEqual(self._get_queryset().count(), initial_count + 1)
            self.assertEqual(self.children[1].pk, response.data[self.child_field][0])

        def test_create_parent_in_storage_location(self):
            """Test that creating a parent FSU with children in a storage location fails."""
            model = self.model._meta.model_name
            data = self.create_data[2]
            data[self.child_field] = [self.children[1].pk]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0].message
            self.assertEqual(
                "Parent FSU must be assigned to a device in order to add child FSUs",
                str(error_message)
            )

        def test_create_parent_with_taken_child(self):
            """Test that creating a parent FSU with a child assigned another parent fails."""
            model = self.model._meta.model_name
            child = self.children[1]
            parent = self.model.objects.first()
            parent.device = Device.objects.last()
            parent.validated_save()

            setattr(child, f"parent_{model}", parent)
            child.validated_save()

            data = self.create_data[0]
            data[self.child_field] = [child.pk]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0].message
            self.assertEqual(
                f"{child._meta.verbose_name} {child.name} is already "
                f"assigned to {getattr(child, f'parent_{model}')}",
                str(error_message)
            )

        def test_clear_children(self):
            """Test that setting child field to an empty list clears the children."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            for child in self.children:
                setattr(child, f"parent_{model}", fsu)
                child.save()

            data = [{"id": str(fsu.pk), self.child_field: []}]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 2)
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 0)

        def test_setting_storage_location_clears_children(self):
            """Test that setting the storage location clears the children."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            for child in self.children:
                setattr(child, f"parent_{model}", fsu)
                child.save()

            data = [{
                "id": str(fsu.pk),
                "location": str(Location.objects.first().pk),
                "status": "available",
            }]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 2)
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 0)

        def test_update_children(self):
            """Test setting a new list of children updates the instances."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            setattr(self.children[1], f"parent_{model}", fsu)
            self.children[1].save()

            data = [{"id": str(fsu.pk), self.child_field: [str(self.children[0].pk)]}]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 1)
            self.assertEqual(getattr(fsu, self.child_field).first(), self.children[1])
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 1)
            self.assertEqual(getattr(fsu, self.child_field).first(), self.children[0])

    class ParentNonFSUChildAPIViewTestCase(FSUAPIViewTestCase):
        """Additional tests for a parent FSU where the children are not FSUs."""

        child_model: Type[ComponentModel]
        child_field: str
        children: list[ComponentModel]

        def test_create_parent_with_child_in_wrong_device(self):
            """Test that creating a parent FSU with a child in a different device fails."""
            model = self.model._meta.model_name
            data = self.create_data[0]
            data[self.child_field] = [str(x.pk) for x in self.children]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0]
            self.assertEqual(
                f"{self.child_model._meta.verbose_name} {self.children[0].name} has a different "
                f"parent device (Device 1-1) than that of its parent FSU (Device 5-2)",
                str(error_message)
            )

        def test_add_parent_with_children(self):
            """Test creating a parent FSU with children."""
            model = self.model._meta.model_name
            data = self.create_data[0]
            data[self.child_field] = [self.children[1].pk]

            initial_count = self._get_queryset().count()
            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_201_CREATED)
            self.assertEqual(self._get_queryset().count(), initial_count + 1)
            self.assertEqual(self.children[1].pk, response.data[self.child_field][0])

        def test_create_parent_in_storage_location(self):
            """Test that creating a parent FSU with children in a storage location fails."""
            model = self.model._meta.model_name
            data = self.create_data[2]
            data[self.child_field] = [self.children[1].pk]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0].message
            self.assertEqual(
                "Parent FSU must be assigned to a device in order to add child FSUs",
                str(error_message)
            )

        def test_create_parent_with_taken_child(self):
            """Test that creating a parent FSU with a child assigned another parent fails."""
            model = self.model._meta.model_name
            child = self.children[1]
            parent = self.model.objects.first()
            parent.device = Device.objects.last()
            parent.validated_save()

            getattr(child, f"parent_{model}").set([parent])

            data = self.create_data[0]
            data[self.child_field] = [child.pk]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            error_message = response.data[self.child_field]
            if isinstance(error_message, list):
                error_message = error_message[0].message
            self.assertEqual(
                f"{child._meta.verbose_name} {child.name} is already "
                f"assigned to {getattr(child, f'parent_{model}').first()}",
                str(error_message)
            )

        def test_clear_children(self):
            """Test that setting child field to an empty list clears the children."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            self.children[1].save()
            for child in self.children:
                getattr(child, f"parent_{model}").set([fsu])

            data = [{"id": str(fsu.pk), self.child_field: []}]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 2)
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 0)

        def test_setting_storage_location_clears_children(self):
            """Test that setting the storage location clears the children."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            self.children[1].save()
            for child in self.children:
                getattr(child, f"parent_{model}").set([fsu])

            data = [{
                "id": str(fsu.pk),
                "location": str(Location.objects.first().pk),
                "status": "available",
            }]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 2)
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 0)

        def test_update_children(self):
            """Test setting a new list of children updates the instances."""
            fsu = self.model.objects.exclude(device__isnull=True).first()
            model = fsu._meta.model_name
            self.children[1].device = fsu.device
            self.children[1].save()
            getattr(self.children[1], f"parent_{model}").set([fsu])

            data = [{"id": str(fsu.pk), self.child_field: [str(self.children[0].pk)]}]
            self.add_permissions(f"nautobot_fsus.change_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")

            self.assertEqual(getattr(fsu, self.child_field).count(), 1)
            self.assertEqual(getattr(fsu, self.child_field).first(), self.children[1])
            response = self.client.patch(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_200_OK)
            self.assertEqual(getattr(fsu, self.child_field).count(), 1)
            self.assertEqual(getattr(fsu, self.child_field).first(), self.children[0])

    class FSUTemplateAPIViewTestCase(APIViewTestCases.APIViewTestCase):
        """Common test case for FSU Template APIs."""
        model: Type[FSUTemplateModel]
        type_model: Type[FSUTypeModel]
        target_model_name: str
        brief_fields = ["display", "id", "name", "url"]

        templates: list[FSUTemplateModel]
        fsu_types: list[FSUTypeModel]

        @classmethod
        def setUpTestData(cls):
            """Create objects and data for the tests."""
            device_type = DeviceType.objects.create(
                manufacturer=Manufacturer.objects.last(),
                model="Test Device Type",
                slug="test-device-type",
            )

            cls.fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test {cls.model._meta.verbose_name}",
                    part_number="0001",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.last(),
                    name=f"Another {cls.model._meta.verbose_name}",
                    part_number="0002",
                ),
            ]

            cls.templates = [
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
                    device_type=DeviceType.objects.first(),
                    name=f"test_{cls.target_model_name.lower()}_01",
                    description=f"First test {cls.target_model_name}",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[1],
                    device_type=DeviceType.objects.last(),
                    name=f"test_{cls.target_model_name.lower()}_02",
                    description=f"Second test {cls.target_model_name}",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
                    device_type=DeviceType.objects.first(),
                    name=f"test_{cls.target_model_name.lower()}_03",
                    description=f"Third test {cls.target_model_name}",
                ),
            ]

            cls.create_data = [
                {
                    "fsu_type": cls.fsu_types[0].pk,
                    "device_type": device_type.pk,
                    "name": f"test_{cls.target_model_name.lower()}_04",
                },
                {
                    "fsu_type": cls.fsu_types[0].pk,
                    "device_type": device_type.pk,
                    "name": f"test_{cls.target_model_name.lower()}_05",
                },
                {
                    "fsu_type": cls.fsu_types[1].pk,
                    "device_type": device_type.pk,
                    "name": f"test_{cls.target_model_name.lower()}_06",
                },
            ]

            cls.bulk_update_data = {"device_type": device_type.id}

        def test_unique_name_per_parent_constraint(self):
            """Test that creating an FSU Template with a duplicate name fails."""
            template = self.model.objects.get(name=self.templates[0].name)
            model = template._meta.model_name
            data = {
                "fsu_type": template.fsu_type.pk,
                "device_type": template.device_type.pk,
                "name": template.name,
            }

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

    class FSUTypeAPIViewTestCase(APIViewTestCases.APIViewTestCase):
        """Common test case for FSU Type APIs."""
        model: Type[FSUTypeModel]
        brief_fields = ["display", "id", "name", "part_number", "url"]

        fsu_types: list[Type[FSUTypeModel]] = []

        @classmethod
        def setUpTestData(cls):
            """Set up the data for the tests."""
            cls.bulk_update_data = {
                "manufacturer": Manufacturer.objects.last().pk
            }

            mfgr = Manufacturer.objects.first()

            for i in range(1, 4):
                cls.fsu_types.append(
                    cls.model.objects.create(
                        manufacturer=mfgr,
                        name=f"Test {cls.model._meta.verbose_name} {i}",
                        part_number=f"000{i}",
                    )
                )

            cls.create_data = [
                {
                    "manufacturer": mfgr.pk,
                    "name": f"Test {cls.model._meta.verbose_name} {i}",
                    "part_number": f"000{i}",
                }
                for i in range(4, 7)
            ]
