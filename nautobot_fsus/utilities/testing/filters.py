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

from nautobot.dcim.models import Device, DeviceRole, DeviceType, Location, Manufacturer
from nautobot.extras.filters import NautobotFilterSet
from nautobot.extras.models import Status
from nautobot.utilities.querysets import RestrictedQuerySet
from nautobot.utilities.testing import FilterTestCases

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
            device_type = DeviceType.objects.create(
                manufacturer=Manufacturer.objects.last(),
                model="Test Device Type",
                slug="test-device-type",
            )
            location = Location.objects.first()
            cls.device = Device.objects.create(
                device_type=device_type,
                device_role=DeviceRole.objects.first(),
                name="Test Device",
                site=location.base_site,
                location=location,
            )

            cls.fsu_types = [
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
                    fsu_type=cls.fsu_types[0],
                    device=cls.device,
                    name=f"test_{ cls.model._meta.model_name }_0",
                    serial_number="a0001",
                    firmware_version="1.0",
                    driver_name="test_driver",
                    driver_version="1.0",
                    description=f"First test { cls.model._meta.verbose_name }",
                    status=Status.objects.get(slug="active"),
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[1],
                    device=cls.device,
                    name=f"test_{ cls.model._meta.model_name }_1",
                    serial_number="a0002",
                    firmware_version="1.1",
                    driver_name="test_driver",
                    driver_version="1.0",
                    description=f"Second test { cls.model._meta.verbose_name }",
                    status=Status.objects.get(slug="active"),
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
                    location=location,
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
            with self.subTest():
                params = {"device_id": [self.device.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest():
                params = {"device": [self.device.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_storage_location(self):
            """Test filtering on the FSU parent storage location."""
            location = Location.objects.first()
            with self.subTest(filter="id"):
                params = {"id": [x.id for x in self.fsus], "location_id": [location.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest(filter="name"):
                params = {"id": [x.id for x in self.fsus], "location": [location.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_fsu_type(self):
            """Test filtering on the FSU type id."""
            fsu_type = self.fsu_types[0]
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

            cls.fsu_types = [
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
                    fsu_type=cls.fsu_types[0],
                    device_type=DeviceType.objects.first(),
                    name=f"test_{ cls.model._meta.model_name }_0",
                    description=f"First test { cls.model._meta.verbose_name } template",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[1],
                    device_type=DeviceType.objects.last(),
                    name=f"test_{ cls.model._meta.model_name }_1",
                    description=f"Second test { cls.model._meta.verbose_name } template",
                ),
                cls.model.objects.create(
                    fsu_type=cls.fsu_types[0],
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
            with self.subTest(filter="id"):
                params = {"device_type_id": [DeviceType.objects.first().id]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest(filte="name"):
                params = {"device_type": [DeviceType.objects.last().slug]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_fsu_type(self):
            """Test filtering on the FSU type."""
            fsu_type = self.fsu_types[0]
            with self.subTest(filter="id"):
                params = {"fsu_type_id": [fsu_type.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
            with self.subTest(filter="name"):
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
            with self.subTest(filter="exact"):
                params = {"part_number": ["A10001"]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest(filter="contains"):
                params = {"part_number__ic": ["A1000"]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

        def test_description(self):
            """Test filtering on the description."""
            params = {"description__ic": ["completely different"]}
            self.assertEqual(self.filterset(params).qs.count(), 1)

        def test_manufacturer(self):
            """Test filtering on the parent manufacturer."""
            manufacturer = Manufacturer.objects.first()
            with self.subTest(filter="id"):
                params = {"id": [x.pk for x in self.types], "manufacturer_id": [manufacturer.pk]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
            with self.subTest(filter="name"):
                params = {"id": [x.pk for x in self.types], "manufacturer": [manufacturer.name]}
                self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        def test_has_instances(self):
            """Test filtering on if the FSU type has instances."""
            self.model.objects.create(
                name=f"test_{ self.model._meta.model_name }",
                fsu_type=self.types[0],
                device=Device.objects.first(),
            )
            with self.subTest(filter="True"):
                params = {"id": [x.pk for x in self.types], "has_instances": True}
                filtered = self.filterset(params, self.queryset).qs
                self.assertEqual(filtered.count(), 1)
                self.assertEqual(filtered.first().name, self.types[0].name)
            with self.subTest(filter="False"):
                params = {"id": [x.pk for x in self.types], "has_instances": False}
                filtered = self.filterset(params, self.queryset).qs
                self.assertEqual(filtered.count(), 1)
                self.assertEqual(filtered.first().name, self.types[1].name)
