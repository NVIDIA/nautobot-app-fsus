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

from django.conf import settings
from nautobot.apps.ui import (
    NavMenuAddButton,
    NavMenuButton,
    NavMenuGroup,
    NavMenuImportButton,
    NavMenuItem,
    NavMenuTab,
)


def item_buttons(model: str) -> list[NavMenuButton]:
    """Confiture the add or add and import buttons, based on version."""
    buttons = [
        NavMenuAddButton(
            link=f"plugins:nautobot_fsus:{model}_add",
            permissions=[f"nautobot_fsus.add_{model}"],
        )
    ]
    # The import button still appears in the menu in Nautobot 2.0.x
    if settings.VERSION_MINOR == 0:
        buttons.append(
            NavMenuImportButton(
                link=f"plugins:nautobot_fsus:{model}_import",
                permissions=[f"nautobot_fsus.add_{model}"],
            )
        )

    return buttons


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
                        permissions=["nautobot_fsus.view_cpu"],
                        buttons=item_buttons("cpu"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:disk_list",
                        name="Disks",
                        permissions=["nautobot_fsus.view_disk"],
                        buttons=item_buttons("disk"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:fan_list",
                        name="Fans",
                        permissions=["nautobot_fsus.view_fans"],
                        buttons=item_buttons("fan"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpu_list",
                        name="GPUs",
                        permissions=["nautobot_fsus.view_gpu"],
                        buttons=item_buttons("gpu"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpubaseboard_list",
                        name="GPU Baseboards",
                        permissions=["nautobot_fsus.view_gpubaseboard"],
                        buttons=item_buttons("gpubaseboard"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:hba_list",
                        name="HBAs",
                        permissions=["nautobot_fsus.view_hba"],
                        buttons=item_buttons("hba"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:mainboard_list",
                        name="Mainboards",
                        permissions=["nautobot_fsus.view_mainboard"],
                        buttons=item_buttons("mainboard"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:nic_list",
                        name="NICs",
                        permissions=["nautobot_fsus.view_nic"],
                        buttons=item_buttons("nic"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:otherfsu_list",
                        name="Other FSUs",
                        permissions=["nautobot_fsus.view_otherfsu"],
                        buttons=item_buttons("otherfsu"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:psu_list",
                        name="PSUs",
                        permissions=["nautobot_fsus.view_psu"],
                        buttons=item_buttons("psu"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:rammodule_list",
                        name="RAM Modules",
                        permissions=["nautobot_fsus.view_rammodule"],
                        buttons=item_buttons("rammodule"),
                    ),
                ],
            ),
            NavMenuGroup(
                name="FSU Types",
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_fsus:cputype_list",
                        name="CPU Types",
                        permissions=["nautobot_fsus.view_cputype"],
                        buttons=item_buttons("cputype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:disktype_list",
                        name="Disk Types",
                        permissions=["nautobot_fsus.view_disktype"],
                        buttons=item_buttons("disktype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:fantype_list",
                        name="Fan Types",
                        permissions=["nautobot_fsus.view_fantype"],
                        buttons=item_buttons("fantype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gputype_list",
                        name="GPU Types",
                        permissions=["nautobot_fsus.view_gputype"],
                        buttons=item_buttons("gputype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:gpubaseboardtype_list",
                        name="GPU Baseboard Types",
                        permissions=["nautobot_fsus.view_gpubaseboardtype"],
                        buttons=item_buttons("gpubaseboardtype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:hbatype_list",
                        name="HBA Types",
                        permissions=["nautobot_fsus.view_hbatype"],
                        buttons=item_buttons("hbatype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:mainboardtype_list",
                        name="Mainboard Types",
                        permissions=["nautobot_fsus.view_mainboardtype"],
                        buttons=item_buttons("mainboardtype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:nictype_list",
                        name="NIC Types",
                        permissions=["nautobot_fsus.view_nictype"],
                        buttons=item_buttons("nictype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:otherfsutype_list",
                        name="Other FSU Types",
                        permissions=["nautobot_fsus.view_otherfsutype"],
                        buttons=item_buttons("otherfsutype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:psutype_list",
                        name="PSU Types",
                        permissions=["nautobot_fsus.view_psutype"],
                        buttons=item_buttons("psutype"),
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_fsus:rammoduletype_list",
                        name="RAM Module Types",
                        permissions=["nautobot_fsus.view_rammoduletype"],
                        buttons=item_buttons("rammoduletype"),
                    ),
                ],
            ),
        ],
    ),
)
