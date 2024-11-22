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

"""Tests for GraphQL queries on FSU and FSU type models."""

from django.test import override_settings
from nautobot.core.graphql import execute_query
from nautobot.utilities.testing import TestCase, create_test_user

from nautobot_fsus import models


class GraphQLTestCase(TestCase):
    """Tests for GraphQL queries."""

    def setUp(self):
        """Create a test user."""
        self.user = create_test_user("graphql_testuser")

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_fsu_graphql(self):
        """Test GraphQL queries on FSU models."""
        for fsu, fsu_model in (
            ("cpus", models.CPU),
            ("disks", models.Disk),
            ("fans", models.Fan),
            ("gpus", models.GPU),
            ("gpu_baseboards", models.GPUBaseboard),
            ("hbas", models.HBA),
            ("nics", models.NIC),
            ("otherfsus", models.OtherFSU),
            ("psus", models.PSU),
            ("ram_modules", models.RAMModule),
        ):
            with self.subTest(fsu=fsu):
                query = f"query {{ {fsu} {{ name }} }}"
                response = execute_query(query, user=self.user)
                self.assertEqual(len(response.data[fsu]), fsu_model.objects.count())

    @override_settings(EXEMPT_VIEW_PERMISSIONS=["*"])
    def test_fsu_type_graphql(self):
        """Test GraphQL queries on FSU type models."""
        for fsu_type, fsu_model in (
            ("cpu_types", models.CPUType),
            ("disk_types", models.DiskType),
            ("fan_types", models.FanType),
            ("gpu_types", models.GPUType),
            ("gpu_baseboard_types", models.GPUBaseboardType),
            ("hba_types", models.HBAType),
            ("nic_types", models.NICType),
            ("other_fsu_types", models.OtherFSUType),
            ("psu_types", models.PSUType),
            ("ram_module_types", models.RAMModuleType),
        ):
            with self.subTest(fsu=fsu_type):
                query = f"query {{ {fsu_type} {{ name }} }}"
                response = execute_query(query, user=self.user)
                self.assertEqual(len(response.data[fsu_type]), fsu_model.objects.count())
