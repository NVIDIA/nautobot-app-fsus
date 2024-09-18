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

"""Test cases and helpers for testing the Nautobot FSUs app."""
from typing import Type

from django.urls import reverse
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer
from nautobot.extras.filters import NautobotFilterSet
from nautobot.extras.models import Status
from nautobot.utilities.querysets import RestrictedQuerySet
from nautobot.utilities.testing import FilterTestCases
from nautobot.utilities.testing.api import APIViewTestCases
from rest_framework import status

from nautobot_fsus.models.mixins import FSUModel, FSUTemplateModel, FSUTypeModel


class FSUFilterTestCases:
    """Wrapper class for FSU filter test cases."""
    # pylint: disable=too-few-public-methods,not-callable

    class FSUModelFilterTestCase(FilterTestCases.FilterTestCase):
        """Common test case for FSU filters."""
        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]
        queryset: RestrictedQuerySet
        filterset: Type[NautobotFilterSet]

        @classmethod
        def setUpTestData(cls):
            """Load initial data for the test case."""
            fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test { cls.model._meta.verbose_name }",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.last(),
                    name=f"Another { cls.model._meta.verbose_name }",
                )
            ]

            cls.fsus = [
                cls.model.objects.create(
                    fsu_type=fsu_types[0],
                    device=Device.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_0",
                    serial_number="a0001",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    description=f"First test { cls.model._meta.verbose_name }",
                    status=Status.objects.get(slug="active"),
                ),
                cls.model.objects.create(
                    fsu_type=fsu_types[1],
                    device=Device.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_1",
                    serial_number="a0002",
                    firmware_version="1.1",
                    driver_name="test_driver",
                    driver_version="1.0",
                    description=f"Second test { cls.model._meta.verbose_name }",
                    status=Status.objects.get(slug="active"),
                ),
                cls.model.objects.create(
                    fsu_type=fsu_types[0],
                    location=Location.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_2",
                    serial_number="b0003",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.1",
                    description=f"Third test { cls.model._meta.verbose_name }",
                    status=Status.objects.get(slug="available"),
                ),
            ]

        def test_name(self):
            """Test filtering on FSU name."""
            params = {"name": self.fsus[:2]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_serial_number(self):
            """Test filtering on the serial_number number."""
            params = {"serial_number": [self.fsus[2].serial_number]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_firmware_version(self):
            """Test filtering on the firmware_version version."""
            params = {"firmware_version": ["1.1"]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_driver_name(self):
            """Test filtering on the FSU driver name."""
            params = {"driver_name": ["test_driver"]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

        def test_driver(self):
            """Test filtering on the FSU driver version."""
            params = {"driver_version": ["1.0"]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_device(self):
            """Test filtering on the FSU parent device."""
            device = Device.objects.first()
            with self.subTest():
                params = {"device_id": [device.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest():
                params = {"device": [device.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_storage_location(self):
            """Test filtering on the FSU parent storage location."""
            location = Location.objects.first()
            with self.subTest():
                params = {"location_id": [location.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest():
                params = {"location": [location.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_fsu_type(self):
            """Test filtering on the FSU type id."""
            fsu_type = self.type_model.objects.first()
            params = {"fsu_type_id": [fsu_type.pk]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    class FSUTemplateFilterTestCase(FilterTestCases.FilterTestCase):
        """Common tests for FSU template filters."""
        model: Type[FSUTemplateModel]
        type_model: Type[FSUTypeModel]
        queryset: RestrictedQuerySet
        filterset: Type[NautobotFilterSet]

        @classmethod
        def setUpTestData(cls):
            """Load/create initial data for the tests."""
            DeviceType.objects.create(
                manufacturer=Manufacturer.objects.last(),
                model="Test Device Type",
                slug="test-device-type",
            )

            fsu_types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test { cls.model._meta.verbose_name }",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.last(),
                    name=f"Another { cls.model._meta.verbose_name }",
                )
            ]

            cls.templates = [
                cls.model.objects.create(
                    fsu_type=fsu_types[0],
                    device_type=DeviceType.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_0",
                    description=f"First test { cls.model._meta.verbose_name } template",
                ),
                cls.model.objects.create(
                    fsu_type=fsu_types[1],
                    device_type=DeviceType.objects.last(),
                    name=f"test_{ cls.model._meta.model_name }_1",
                    description=f"Second test { cls.model._meta.verbose_name } template",
                ),
                cls.model.objects.create(
                    fsu_type=fsu_types[0],
                    device_type=DeviceType.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_2",
                    description=f"Third test { cls.model._meta.verbose_name } template",
                ),
            ]

        def test_name(self):
            """Test filtering on FSU template name."""
            params = {"name": [x.name for x in self.templates[:2]]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_pci_slot_id(self):
            """Test filtering on the PCI slot ID."""
            if not hasattr(self.model, "pci_slot_id"):
                self.skipTest("Template does not have PCI slot id.")

            params = {"pci_slot_id": [self.templates[0].pci_slot_id]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_device_type(self):
            """Test filtering on the DeviceType."""
            with self.subTest():
                params = {"device_type_id": [DeviceType.objects.first().id]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest():
                params = {"device_type": [DeviceType.objects.last().slug]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_fsu_type(self):
            """Test filtering on the FSU type."""
            fsu_type = self.type_model.objects.first()
            with self.subTest():
                params = {"fsu_type_id": [fsu_type.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest():
                params = {"fsu_type": [fsu_type.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_description(self):
            """Test filtering on the FSU template description."""
            params = {"description": [self.templates[2].description]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    class FSUTypeFilterTestCase(FilterTestCases.FilterTestCase):
        """Common tests for FSU type filters."""
        model: Type[FSUModel]
        type_model: Type[FSUTypeModel]
        queryset: RestrictedQuerySet
        filterset: Type[NautobotFilterSet]

        @classmethod
        def setUpTestData(cls):
            """Load initial data for the test case."""
            cls.types = [
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.first(),
                    name=f"Test { cls.model._meta.object_name }",
                    part_number="A10001",
                    description=f"{ cls.model._meta.object_name } for testing.",
                ),
                cls.type_model.objects.create(
                    manufacturer=Manufacturer.objects.last(),
                    name=f"Another { cls.model._meta.object_name }",
                    part_number="A10002",
                    description=f"A completely different { cls.model._meta.object_name }.",
                ),
            ]

        def test_model_name(self):
            """Test filtering on the model name."""
            params = {"name": [self.types[0].name]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_part_number(self):
            """Test filtering on the part number."""
            with self.subTest():
                params = {"part_number": ["A10001"]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest():
                params = {"part_number__ic": ["A1000"]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_description(self):
            """Test filtering on the description."""
            params = {"description__ic": ["completely different"]}
            self.assertEqual(self.filterset(params).qs.count(), 1)

        def test_manufacturer(self):
            """Test filtering on the parent manufacturer."""
            manufacturer = Manufacturer.objects.first()
            with self.subTest():
                params = {"manufacturer_id": [manufacturer.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest():
                params = {"manufacturer": [manufacturer.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_has_instances(self):
            """Test filtering on if the FSU type has instances."""
            self.model.objects.create(
                name=f"test_{ self.model._meta.model_name }",
                fsu_type=self.type_model.objects.first(),
                device=Device.objects.first(),
            )
            with self.subTest():
                params = {"has_instances": True}
                filtered = self.filterset(params, self.queryset).qs
                self.assertEqual(filtered.count(), 1)
                self.assertEqual(filtered.first().name, self.types[0].name)
            with self.subTest():
                params = {"has_instances": False}
                filtered = self.filterset(params, self.queryset).qs
                self.assertEqual(filtered.count(), 1)
                self.assertEqual(filtered.first().name, self.types[1].name)


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
            self.assertEqual(
                f"{self.child_model._meta.verbose_name} {self.children[0].name} has a different "
                f"parent device (Device 1-1) than that of its parent FSU (Device 5-2)",
                str(response.data[self.child_field])
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
            self.assertEqual(
                "Parent FSU must be assigned to a device in order to add child FSUs",
                str(response.data[self.child_field])
            )

        def test_create_parent_with_taken_child(self):
            """Test that creating a parent FSU with a child assigned another parent fails."""
            model = self.model._meta.model_name
            child = self.children[1]
            setattr(child, f"parent_{model}", self.model.objects.first())
            child.validated_save()

            data = self.create_data[0]
            data[self.child_field] = [child.pk]

            self.add_permissions(f"nautobot_fsus.add_{ model }")
            url = reverse(f"plugins-api:nautobot_fsus-api:{ model }-list")
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIsInstance(response.data, dict)
            self.assertIn(self.child_field, response.data)
            self.assertEqual(
                f"{child._meta.verbose_name} {child.name} is already "
                f"assigned to {getattr(child, f'parent_{model}')}",
                str(response.data[self.child_field])
            )

        def test_clear_children(self):
            """Test that setting child field to an empty list clears the children."""
            fsu = self.model.objects.first()
            model = fsu._meta.model_name
            self.children[1].device = Device.objects.first()
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
            fsu = self.model.objects.first()
            model = fsu._meta.model_name
            self.children[1].device = Device.objects.first()
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
            fsu = self.model.objects.first()
            model = fsu._meta.model_name
            self.children[1].device = Device.objects.first()
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
                "manufacturer": Manufacturer.objects.get(slug="manufacturer-2").id
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
