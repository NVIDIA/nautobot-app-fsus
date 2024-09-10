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

"""Routes and url patterns for the Nautobot FSUs app."""
from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.core.views.routers import NautobotUIViewSetRouter

from nautobot_fsus import views

router = NautobotUIViewSetRouter()
router.register("cpus", views.CPUUIViewSet)
router.register("cpu-templates", views.CPUTemplateUIViewSet)
router.register("cpu-types", views.CPUTypeUIViewSet)
router.register("disks", views.DiskUIViewSet)
router.register("disk-templates", views.DiskTemplateUIViewSet)
router.register("disk-types", views.DiskTypeUIViewSet)
router.register("fans", views.FanUIViewSet)
router.register("fan-templates", views.FanTemplateUIViewSet)
router.register("fan-types", views.FanTypeUIViewSet)
router.register("gpus", views.GPUUIViewSet)
router.register("gpu-templates", views.GPUTemplateUIViewSet)
router.register("gpu-types", views.GPUTypeUIViewSet)
router.register("gpubaseboards", views.GPUBaseboardUIViewSet)
router.register("gpubaseboard-templates", views.GPUBaseboardTemplateUIViewSet)
router.register("gpubaseboard-types", views.GPUBaseboardTypeUIViewSet)
router.register("hbas", views.HBAUIViewSet)
router.register("hba-templates", views.HBATemplateUIViewSet)
router.register("hbatypes", views.HBATypeUIViewSet)
router.register("mainboards", views.MainboardUIViewSet)
router.register("mainboard-templates", views.MainboardTemplateUIViewSet)
router.register("mainboard-types", views.MainboardTypeUIViewSet)
router.register("nics", views.NICUIViewSet)
router.register("nic-templates", views.NICTemplateUIViewSet)
router.register("nic-types", views.NICTypeUIViewSet)
router.register("otherfsus", views.OtherFSUUIViewSet)
router.register("otherfsu-templates", views.OtherFSUTemplateUIViewSet)
router.register("otherfsu-types", views.OtherFSUTypeUIViewSet)
router.register("psus", views.PSUUIViewSet)
router.register("psu-templates", views.PSUTemplateUIViewSet)
router.register("psu-types", views.PSUTypeUIViewSet)
router.register("rammodules", views.RAMModuleUIViewSet)
router.register("rammodule-templates", views.RAMModuleTemplateUIViewSet)
router.register("rammodule-types", views.RAMModuleTypeUIViewSet)

urlpatterns = [
    path("cpus/rename/", views.CPUBulkRenameView.as_view(), name="cpu_bulk_rename"),
    path("devices/<uuid:pk>/fsus/", views.DeviceFSUViewTab.as_view(), name="device_fsus_tab"),
    path("docs/", RedirectView.as_view(url=static("nautobot_fsus/docs/index.html")), name="docs"),
    path("disks/rename/", views.DiskBulkRenameView.as_view(), name="disk_bulk_rename"),
    path("fans/rename/", views.FanBulkRenameView.as_view(), name="fan_bulk_rename"),
    path("gpus/rename/", views.GPUBulkRenameView.as_view(), name="gpu_bulk_rename"),
    path(
        "gpubaseboards/rename/",
        views.GPUBaseboardBulkRenameView.as_view(),
        name="gpubaseboard_bulk_rename",
    ),
    path("hbas/rename/", views.HBABulkRenameView.as_view(), name="hba_bulk_rename"),
    path("locations/<uuid:pk>/fsus/", views.LocationFSUViewTab.as_view(), name="location_fsus_tab"),
    path(
        "mainboards/rename/",
        views.MainboardBulkRenameView.as_view(),
        name="mainboard_bulk_rename",
    ),
    path("nics/rename/", views.NICBulkRenameView.as_view(), name="nic_bulk_rename"),
    path("otherfsus/rename/", views.OtherFSUBulkRenameView.as_view(), name="otherfsu_bulk_rename"),
    path("psus/rename/", views.PSUBulkRenameView.as_view(), name="psu_bulk_rename"),
    path(
        "rammodules/rename/",
        views.RAMModuleBulkRenameView.as_view(),
        name="rammodule_bulk_rename",
    ),
]

urlpatterns += router.urls
