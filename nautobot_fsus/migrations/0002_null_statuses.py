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

from django.db import migrations
from nautobot.extras.utils import fixup_null_statuses


def update_statuses(apps, *args, **kwargs):
    """Run fixup_null_statuses on all FSU classes."""
    status_model = apps.get_model("extras", "Status")
    content_type = apps.get_model("contenttypes", "ContentType")

    for model_name in (
        "CPU",
        "Disk",
        "Fan",
        "GPU",
        "GPUBaseboard",
        "HBA",
        "Mainboard",
        "NIC",
        "OtherFSU",
        "PSU",
        "RAMModule",
    ):
        model = apps.get_model("nautobot_fsus", model_name)
        model_content_type = content_type.objects.get_for_model(model)
        fixup_null_statuses(
            model=model,
            model_contenttype=model_content_type,
            status_model=status_model,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0099_remove_dangling_note_objects"),
        ("nautobot_fsus", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_statuses, migrations.RunPython.noop),
    ]
