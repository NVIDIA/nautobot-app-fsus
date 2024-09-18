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

"""URL routes for FSU API endpoint views."""
from nautobot.core.api import OrderedDefaultRouter

from nautobot_fsus.api import views


router = OrderedDefaultRouter()

router.register("cpus", views.CPUAPIView)
router.register("cpu-templates", views.CPUTemplateAPIView)
router.register("cpu-types", views.CPUTypeAPIView)
router.register("disks", views.DiskAPIView)
router.register("disk-templates", views.DiskTemplateAPIView)
router.register("disk-types", views.DiskTypeAPIView)
router.register("fans", views.FanAPIView)
router.register("fan-templates", views.FanTemplateAPIView)
router.register("fan-types", views.FanTypeAPIView)
router.register("gpubaseboards", views.GPUBaseboardAPIView)
router.register("gpubaseboard-templates", views.GPUBaseboardTemplateAPIView)
router.register("gpubaseboard-types", views.GPUBaseboardTypeAPIView)
router.register("gpus", views.GPUAPIView)
router.register("gpu-templates", views.GPUTemplateAPIView)
router.register("gpu-types", views.GPUTypeAPIView)
router.register("hbas", views.HBAAPIView)
router.register("hba-templates", views.HBATemplateAPIView)
router.register("hba-types", views.HBATypeAPIView)
router.register("mainboards", views.MainboardAPIView)
router.register("mainboard-templates", views.MainboardTemplateAPIView)
router.register("mainboard-types", views.MainboardTypeAPIView)
router.register("nics", views.NICAPIView)
router.register("nic-templates", views.NICTemplateAPIView)
router.register("nic-types", views.NICTypeAPIView)
router.register("otherfsus", views.OtherFSUAPIView)
router.register("otherfsu-templates", views.OtherFSUTemplateAPIView)
router.register("otherfsu-types", views.OtherFSUTypeAPIView)
router.register("psus", views.PSUAPIView)
router.register("psu-templates", views.PSUTemplateAPIView)
router.register("psu-types", views.PSUTypeAPIView)
router.register("rammodules", views.RAMModuleAPIView)
router.register("rammodule-templates", views.RAMModuleTemplateAPIView)
router.register("rammodule-types", views.RAMModuleTypeAPIView)

app_name = "nautobot_fsus-api"
urlpatterns = router.urls
