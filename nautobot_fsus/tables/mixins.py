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
from typing import Any

from django.urls import reverse
from django.utils.html import format_html
import django_tables2 as tables
from nautobot.apps.tables import (
    BaseTable,
    ButtonsColumn,
    LinkedCountColumn,
    StatusTableMixin,
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


class KludgeLinkedCountColumn(LinkedCountColumn):
    """
    Fixed version of LinkedCountColumn to deal with the bug in Nautobot 2.3.x.

    Here's the deal. Nautobot 2.3 broke the LinkedCountColumn for apps/plugins by changing a
    lookup so that mapping the columns view to its model only works for non-plugin models.
    Setting the `viewname` parameter without "plugins:" fixes the mapping, in theory, but doing
    that breaks the view lookup for the link in the column. This hijacked class is the only way
    to work around it.
    """

    def __init__(self, viewname: str, *args: Any, view_kwargs: dict[str, Any] | None = None,
                 url_params: dict[str, str] | None = None, default: int = 0, **kwargs: Any) -> None:
        """Initialize the column with view name fix."""
        # drop the "plugins:" from the front of the view name, since it's easier to deal with the
        # column render method than the table lookup to map the view to a model.
        viewname = ":".join(viewname.split(":")[1:])
        super().__init__(
            viewname,
            *args,
            view_kwargs=view_kwargs,
            url_params=url_params,
            default=default,
            **kwargs
        )

    def render(self, record: Any, value: str | None) -> str | None:
        """Render the field value in the column."""
        if value:
            url = [reverse(f"plugins:{self.viewname}", kwargs=self.view_kwargs)]
            if self.url_params:
                url.append("?")
                url.append(
                    "&".join([f"{k}={getattr(record, v)}" for k, v in self.url_params.items()])
                )
                return format_html('<a href="{}">{}</a>', "".join(url), value)
        return value


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
