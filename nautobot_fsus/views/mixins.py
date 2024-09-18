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

"""Base view classes for Nautobot FSU app models."""
from copy import deepcopy
from typing import Any, Type

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.http.request import HttpRequest
from django.template.loader import select_template, TemplateDoesNotExist
from nautobot.core.views.generic import BulkRenameView
from nautobot.core.views.viewsets import NautobotUIViewSet
from nautobot.dcim.models import DeviceType
from nautobot.utilities.permissions import resolve_permission
from nautobot.utilities.tables import BaseTable
from rest_framework.response import Response

from nautobot_fsus.forms.mixins import FSUTemplateCreateForm, FSUTemplateModelForm


class FSUBulkRenameView(BulkRenameView):
    """Bulk rename view that includes the parent name."""
    def get_selected_objects_parents_name(self, selected_objects):
        """Return the parent Device or Location name."""
        selected_object = selected_objects.first()
        # Model constraints should prevent an FSU from being created without
        # a parent, but just in case...
        return selected_object.parent.name if selected_object.parent else ""


class FSUModelViewSet(NautobotUIViewSet):
    """Base viewset for FSU models."""

    base_template = "nautobot_fsus/fsu.html"
    bulk_table_class: Type[BaseTable]

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Override the `fields` context in bulk_create requests."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "bulk_create" and hasattr(self, "bulk_create_form_class"):
            fields = self.bulk_create_form_class().fields  # pylint: disable=not-callable
            fields["device"].required = True
            fields["location"].required = True
            context["fields"] = fields

        return context

    def get_form_class(self, **kwargs):
        """Override default headers for csv imports."""
        form_class = super().get_form_class(**kwargs)
        if self.action == "bulk_create":
            initial = form_class.base_fields["csv_data"].initial
            help_text = form_class.base_fields["csv_data"].help_text
            form_class.base_fields["csv_data"].initial = f"device,location,{initial}"
            form_class.base_fields["csv_data"].help_text = (
                f"{help_text} Note that one of either a `device` or a `location` (but not "
                f"both) is required."
            )

        return form_class

    def get_table_class(self) -> BaseTable:
        """Get the appropriate table class for the view."""
        if self.action.startswith("bulk"):
            return self.bulk_table_class

        return super().get_table_class()

    def get_template_name(self) -> str:
        """Determine the appropriate template name for a request."""
        if self.action == "retrieve":
            return "nautobot_fsus/fsu.html"

        try:
            template_name = f"nautobot_fsus/fsu_{self.action}.html"
            select_template([template_name])
        except TemplateDoesNotExist:
            template_name = super().get_template_name()

        return template_name

    def get_template_names(self) -> list[str]:
        """Determine the appropriate template names for a request."""
        template_name = self.get_template_name()
        return [template_name]


class FSUTemplateModelViewSet(NautobotUIViewSet):
    """Base viewset for FSUTemplate models."""

    base_template = "nautobot_fsus/fsu_template.html"

    def _get_new_fsus(
        self,
        request: HttpRequest,
        form: FSUTemplateCreateForm,
    ) -> tuple[list[FSUTemplateModelForm], FSUTemplateCreateForm]:
        """Break out the new FSUTemplates to add into separate model forms."""
        # pylint: disable=too-many-locals
        new_fsus = []
        data = deepcopy(request.POST)

        names = form.cleaned_data["name_pattern"]
        pci_slot_ids = form.cleaned_data.get("pci_slot_id_pattern")
        slot_ids = form.cleaned_data.get("slot_id_pattern")
        for i, name in enumerate(names):
            pci_slot_id = pci_slot_ids[i] if pci_slot_ids else None
            slot_id = slot_ids[i] if slot_ids else None
            data["name"] = name
            if pci_slot_id is not None:
                data["pci_slot_id"] = pci_slot_id
            if slot_id is not None:
                data["slot_id"] = slot_id
            fsu_form = self.form_class(data)  # pylint: disable=not-callable

            if fsu_form.is_valid():
                new_fsus.append(fsu_form)
            else:
                for field, errors in fsu_form.errors.as_data().items():
                    if field == "name":
                        field = "name_pattern"
                    elif field == "pci_slot_id":
                        field = "pci_slot_id_pattern"
                    elif field == "slot_id":
                        field = "slot_id_pattern"
                    for error in errors:
                        err_string = ", ".join(error)
                        form.add_error(field, f"{name}: {err_string}")

        return new_fsus, form

    def get_extra_context(self, request, instance=None) -> dict[str, Any]:
        """Add the model form and parent DeviceType."""
        context: dict[str, Any] = super().get_extra_context(request, instance)

        if self.action == "create":
            parent = DeviceType.objects.filter(pk=request.GET.get("device_type")).first()
            model_form = self.form_class(request.GET)  # pylint: disable=not-callable
            context.update({"model_form": model_form, "parent": parent})

        return context

    def check_permissions(self, request):
        """Make sure object-level permissions are checked."""
        user = self.request.user
        permission_required = self.get_required_permission()

        for permission in permission_required:
            if user.has_perms([permission]):
                action = resolve_permission(permission)[1]
                self.queryset = self.queryset.restrict(user, action)

            else:
                self.permission_denied(
                    request,
                    message=getattr(permission, "message", None),
                    code=getattr(permission, "code", None),
                )

    def get_template_name(self) -> str:
        """Determine the appropriate template name for a request."""
        if self.action == "retrieve":
            return self.base_template

        try:
            template_name = f"nautobot_fsus/fsu_template_{self.action}.html"
            select_template([template_name])
        except TemplateDoesNotExist:
            template_name = super().get_template_name()

        return template_name

    def get_template_names(self) -> list[str]:
        """Determine the appropriate template names for a request."""
        template_name = self.get_template_name()
        return [template_name]

    def perform_create(self, request, *args, **kwargs):
        """Validate the form and create the new FSU template(s)."""
        form = self.create_form_class(request.POST, initial=request.GET)  # pylint: disable=not-callable
        model_form = self.form_class(request.POST)  # pylint: disable=not-callable
        parent = DeviceType.objects.filter(
            pk=request.GET.get("device_type", request.POST.get("device_type"))
        ).first()

        if form.is_valid():
            new_fsus, form = self._get_new_fsus(request, form)

            if not form.errors:
                try:
                    with transaction.atomic():
                        new_objects = []
                        for fsu_form in new_fsus:
                            obj = fsu_form.save()
                            new_objects.append(obj)

                        if (self.queryset.filter(pk__in=[obj.pk for obj in new_objects]).count()
                                != len(new_objects)):
                            raise ObjectDoesNotExist

                    message = (f"Added {len(new_objects)} "
                               f"{self.queryset.model._meta.verbose_name_plural}")
                    self.logger.info(message)
                    messages.success(request, message)

                    if "_addanother" in request.POST:
                        return HttpResponseRedirect(request.get_full_path())

                    return HttpResponseRedirect(self.get_return_url(request))

                except ObjectDoesNotExist:
                    message = (f"{self.queryset.model._meta.verbose_name} creation failed due to "
                               f"object-level permissions violation.")
                    self.logger.info(message)
                    form.add_error(None, message)

        return Response({"form": form, "model_form": model_form, "parent": parent})


class FSUTypeModelViewSet(NautobotUIViewSet):
    """Base viewset for FSUType models."""

    base_template = "nautobot_fsus/fsu_type.html"

    def get_template_name(self) -> str:
        """Determine the appropriate template name for a request."""
        if self.action == "retrieve":
            return "nautobot_fsus/fsu_type.html"

        try:
            template_name = f"nautobot_fsus/fsu_type_{self.action}.html"
            select_template([template_name])
        except TemplateDoesNotExist:
            template_name = super().get_template_name()

        return template_name

    def get_template_names(self) -> list[str]:
        """Determine the appropriate template names for a request."""
        template_name = self.get_template_name()
        return [template_name]
