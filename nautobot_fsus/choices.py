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

"""Choice sets for FSUs and Consumables models and forms."""
from nautobot.utilities.choices import ChoiceSet


class CPUArchitectures(ChoiceSet):
    """Choice set for CPU architectures."""
    x86 = "x86"
    arm = "arm"
    other = "o"

    CHOICES = [
        (x86, "X86"),
        (arm, "Arm"),
        (other, "Other"),
    ]


class DiskTypes(ChoiceSet):
    """Choice set for types of disks used in devices."""
    disk_hdd = "HDD"
    disk_ssd = "SSD"
    disk_nvme = "NVME"
    other = "o"

    CHOICES = [
        (disk_hdd, "HDD"),
        (disk_ssd, "SSD"),
        (disk_nvme, "NVME"),
        (other, "Other"),
    ]


class MemoryModuleTypes(ChoiceSet):
    """Module types for memory units."""
    # pylint: disable=invalid-name
    lrdimm = "l"
    rdimm = "r"
    rdimm_vlp = "rv"
    sodimm = "s"
    sodimm_ecc = "se"
    udimm = "u"
    udimm_ecc = "ue"
    udimm_vlp_ecc = "uve"
    other = "o"

    CHOICES = [
        (lrdimm, "LRDIMM"),
        (rdimm, "RDIMM"),
        (rdimm_vlp, "VLP RDIMM"),
        (sodimm, "SODIMM"),
        (sodimm_ecc, "ECC SODIMM"),
        (udimm, "UDIMM"),
        (udimm_ecc, "ECC UDIMM"),
        (udimm_vlp_ecc, "VLP ECC UDIMM"),
        (other, "Other"),
    ]


class MemoryTechnologies(ChoiceSet):
    """Memory technology."""
    # pylint: disable=invalid-name
    ddr = "ddr"
    ddr2 = "ddr2"
    ddr3 = "ddr3"
    ddr3l = "ddr3l"
    ddr4 = "ddr4"
    ddr5 = "ddr5"
    other = "o"

    CHOICES = [
        (ddr, "DDR"),
        (ddr2, "DDR2"),
        (ddr3, "DDR3"),
        (ddr3l, "DDR3L"),
        (ddr4, "DDR4"),
        (ddr5, "DDR5"),
    ]


class PCIeGenerations(ChoiceSet):
    """Mainboard PCIe generations."""
    gen1 = 1
    gen2 = 2
    gen3 = 3
    gen4 = 4
    gen5 = 5
    gen6 = 6
    gen7 = 7
    gen8 = 8
    gen9 = 9
    gen10 = 10
    other = 0

    CHOICES = [
        (None, None),
        (gen1, "1.x"),
        (gen2, "2.x"),
        (gen3, "3.x"),
        (gen4, "4.x"),
        (gen5, "5.x"),
        (gen6, "6.x"),
        (gen7, "7.x"),
        (gen8, "8.x"),
        (gen9, "9.x"),
        (gen10, "10.x"),
        (other, "Other"),
    ]


class PSUFeedType(ChoiceSet):
    """Power feed types used by a PSU."""
    psu_ac = "ac"
    psu_dc = "dc"
    psu_switchable = "switchable"

    CHOICES = [
        (psu_ac, "AC"),
        (psu_dc, "DC"),
        (psu_switchable, "Switchable"),
    ]
