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

"""Table mixins and base classes to handle user-definable fields for FSU and FSUTypes models."""
import django_tables2 as tables
from nautobot.extras.tables import StatusTableMixin
from nautobot.utilities.tables import (
    BaseTable,
    ButtonsColumn,
    LinkedCountColumn,
    TagColumn,
    ToggleColumn,
)


class FSUModelTable(StatusTableMixin, BaseTable):
    """Base class for FSU tables."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    parent = tables.TemplateColumn("{{ record.parent }}", linkify=True)
    actions: ButtonsColumn
    tags: TagColumn

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """FSUModelTable model options."""

        abstract = True
        fields = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_name",
            "driver_version",
            "asset_tag",
            "status",
            "description",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "parent",
            "fsu_type",
            "firmware_version",
            "status",
            "actions",
        ]


class FSUTemplateModelTable(BaseTable):
    """Base class for FSU template tables."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True, order_by=("_name",))
    device_type = tables.Column(linkify=True)
    actions: ButtonsColumn

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """FSUTemplateModelTable model options."""

        abstract = True
        fields = [
            "pk",
            "name",
            "fsu_type",
            "device_type",
            "description",
            "actions",
        ]


class FSUTypeModelTable(BaseTable):
    """Base class for FSU type tables."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    manufacturer = tables.Column(linkify=True)
    instance_count: LinkedCountColumn
    tags: TagColumn
    actions: ButtonsColumn

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """FSUTypeModelTable model options."""

        abstract = True
        fields = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "description",
            "instance_count",
            "tags",
            "actions",
        ]
        default_columns = [
            "pk",
            "name",
            "manufacturer",
            "part_number",
            "description",
            "instance_count",
            "actions",
        ]
