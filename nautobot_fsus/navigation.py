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

"""Add FSUs to the navigation menu."""

from nautobot.core.apps import (
    NavMenuAddButton,
    NavMenuGroup,
    NavMenuImportButton,
    NavMenuItem,
    NavMenuTab,
)

menu_items = (
    NavMenuTab(
        name="FSUs",
        groups=[
            NavMenuGroup(
                name="Field Serviceable Units",
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_fsus:cpu_list",
                        name="CPUs",
                        permissions=["nautobot_fsus:view_cpu"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:cpu_add",
                                permissions=["nautobot_fsus:add_cpu"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:cpu_import",
                                permissions=["nautobot_fsus:add_cpu"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:disk_list",
                        name="Disks",
                        permissions=["nautobot_fsus:view_disk"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:disk_add",
                                permissions=["nautobot_fsus:add_disk"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:disk_import",
                                permissions=["nautobot_fsus:add_disk"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:fan_list",
                        name="Fans",
                        permissions=["nautobot_fsus:view_fans"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:fan_add",
                                permissions=["nautobot_fsus:add_fan"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:fan_import",
                                permissions=["nautobot_fsus:add_fan"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpu_list",
                        name="GPUs",
                        permissions=["nautobot_fsus:view_gpu"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:gpu_add",
                                permissions=["nautobot_fsus:add_gpu"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:gpu_import",
                                permissions=["nautobot_fsus:add_gpu"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpubaseboard_list",
                        name="GPU Baseboards",
                        permissions=["nautobot_fsus:view_gpubaseboard"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:gpubaseboard_add",
                                permissions=["nautobot_fsus:add_gpubaseboard"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:gpubaseboard_import",
                                permissions=["nautobot_fsus:add_gpubaseboard"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:hba_list",
                        name="HBAs",
                        permissions=["nautobot_fsus:view_hba"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:hba_add",
                                permissions=["nautobot_fsus:add_hba"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:hba_import",
                                permissions=["nautobot_fsus:add_hba"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:mainboard_list",
                        name="Mainboards",
                        permissions=["nautobot_fsus:view_mainboard"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:mainboard_add",
                                permissions=["nautobot_fsus:add_mainboard"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:mainboard_import",
                                permissions=["nautobot_fsus:add_mainboard"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:nic_list",
                        name="NICs",
                        permissions=["nautobot_fsus:view_nic"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:nic_add",
                                permissions=["nautobot_fsus:add_nic"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:nic_import",
                                permissions=["nautobot_fsus:add_nic"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:otherfsu_list",
                        name="Other FSUs",
                        permissions=["nautobot_fsus:view_otherfsu"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:otherfsu_add",
                                permissions=["nautobot_fsus:add_otherfsu"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:otherfsu_import",
                                permissions=["nautobot_fsus:add_otherfsu"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:psu_list",
                        name="PSUs",
                        permissions=["nautobot_fsus:view_psu"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:psu_add",
                                permissions=["nautobot_fsus:add_psu"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:psu_import",
                                permissions=["nautobot_fsus:add_psu"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:rammodule_list",
                        name="RAM Modules",
                        permissions=["nautobot_fsus:view_rammodule"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:rammodule_add",
                                permissions=["nautobot_fsus:add_rammodule"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:rammodule_import",
                                permissions=["nautobot_fsus:add_rammodule"],
                            ),
                        ],
                    ),
                ],
            ),
            NavMenuGroup(
                name="FSU Types",
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_fsus:cputype_list",
                        name="CPU Types",
                        permissions=["nautobot_fsus:view_cputype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:cputype_add",
                                permissions=["nautobot_fsus:add_cputype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:cputype_import",
                                permissions=["nautobot_fsus:add_cputype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:disktype_list",
                        name="Disk Types",
                        permissions=["nautobot_fsus:view_disktype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:disktype_add",
                                permissions=["nautobot_fsus:add_disktype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:disktype_import",
                                permissions=["nautobot_fsus:add_disktype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:fantype_list",
                        name="Fan Types",
                        permissions=["nautobot_fsus:view_fantype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:fantype_add",
                                permissions=["nautobot_fsus:add_fantype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:fantype_import",
                                permissions=["nautobot_fsus:add_fantype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gputype_list",
                        name="GPU Types",
                        permissions=["nautobot_fsus:view_gputype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:gputype_add",
                                permissions=["nautobot_fsus:add_gputype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:gputype_import",
                                permissions=["nautobot_fsus:add_gputype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpubaseboardtype_list",
                        name="GPU Baseboard Types",
                        permissions=["nautobot_fsus:view_gpubaseboardtype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:gpubaseboardtype_add",
                                permissions=["nautobot_fsus:add_gpubaseboardtype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:gpubaseboardtype_import",
                                permissions=["nautobot_fsus:add_gpubaseboardtype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:hbatype_list",
                        name="HBA Types",
                        permissions=["nautobot_fsus:view_hbatype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:hbatype_add",
                                permissions=["nautobot_fsus:add_hbatype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:hbatype_import",
                                permissions=["nautobot_fsus:add_hbatype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:mainboardtype_list",
                        name="Mainboard Types",
                        permissions=["nautobot_fsus:view_mainboardtype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:mainboardtype_add",
                                permissions=["nautobot_fsus:add_mainboardtype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:mainboardtype_import",
                                permissions=["nautobot_fsus:add_mainboardtype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:nictype_list",
                        name="NIC Types",
                        permissions=["nautobot_fsus:view_nictype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:nictype_add",
                                permissions=["nautobot_fsus:add_nictype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:nictype_import",
                                permissions=["nautobot_fsus:add_nictype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:otherfsutype_list",
                        name="Other FSU Types",
                        permissions=["nautobot_fsus:view_otherfsutype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:otherfsutype_add",
                                permissions=["nautobot_fsus:add_otherfsutype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:otherfsutype_import",
                                permissions=["nautobot_fsus:add_otherfsutype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:psutype_list",
                        name="PSU Types",
                        permissions=["nautobot_fsus:view_psutype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:psutype_add",
                                permissions=["nautobot_fsus:add_psutype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:psutype_import",
                                permissions=["nautobot_fsus:add_psutype"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:rammoduletype_list",
                        name="RAM Module Types",
                        permissions=["nautobot_fsus:view_rammoduletype"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_fsus:rammoduletype_add",
                                permissions=["nautobot_fsus:add_rammoduletype"],
                            ),
                            NavMenuImportButton(
                                link="plugins:nautobot_fsus:rammoduletype_import",
                                permissions=["nautobot_fsus:add_rammoduletype"],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    ),
)
