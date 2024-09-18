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

"""View definitions for FSUTemplate models."""
from nautobot_fsus import filters, forms, models, tables
from nautobot_fsus.api import serializers
from nautobot_fsus.views.mixins import FSUTemplateModelViewSet


class CPUTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for CPUTemplate model."""

    bulk_create_form_class = forms.CPUTemplateCSVForm
    bulk_update_form_class = forms.CPUTemplateBulkEditForm
    create_form_class = forms.CPUTemplateCreateForm
    filterset_class = filters.CPUTemplateFilterSet
    form_class = forms.CPUTemplateForm
    lookup_field = "pk"
    queryset = models.CPUTemplate.objects.all()
    serializer_class = serializers.CPUTemplateSerializer
    table_class = tables.CPUTemplateTable


class DiskTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for DiskTemplate model."""

    bulk_create_form_class = forms.DiskTemplateCSVForm
    bulk_update_form_class = forms.DiskTemplateBulkEditForm
    create_form_class = forms.DiskTemplateCreateForm
    filterset_class = filters.DiskTemplateFilterSet
    form_class = forms.DiskTemplateForm
    lookup_field = "pk"
    queryset = models.DiskTemplate.objects.all()
    serializer_class = serializers.DiskTemplateSerializer
    table_class = tables.DiskTemplateTable


class FanTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for FanTemplate model."""

    bulk_create_form_class = forms.FanTemplateCSVForm
    bulk_update_form_class = forms.FanTemplateBulkEditForm
    create_form_class = forms.FanTemplateCreateForm
    filterset_class = filters.FanTemplateFilterSet
    form_class = forms.FanTemplateForm
    lookup_field = "pk"
    queryset = models.FanTemplate.objects.all()
    serializer_class = serializers.FanTemplateSerializer
    table_class = tables.FanTemplateTable


class GPUTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for GPUTemplate model."""

    bulk_create_form_class = forms.GPUTemplateCSVForm
    bulk_update_form_class = forms.GPUTemplateBulkEditForm
    create_form_class = forms.GPUTemplateCreateForm
    filterset_class = filters.GPUTemplateFilterSet
    form_class = forms.GPUTemplateForm
    lookup_field = "pk"
    queryset = models.GPUTemplate.objects.all()
    serializer_class = serializers.GPUTemplateSerializer
    table_class = tables.GPUTemplateTable


class GPUBaseboardTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for GPUBaseboardTemplate model."""

    bulk_create_form_class = forms.GPUBaseboardTemplateCSVForm
    bulk_update_form_class = forms.GPUBaseboardTemplateBulkEditForm
    create_form_class = forms.GPUBaseboardTemplateCreateForm
    filterset_class = filters.GPUBaseboardTemplateFilterSet
    form_class = forms.GPUBaseboardTemplateForm
    lookup_field = "pk"
    queryset = models.GPUBaseboardTemplate.objects.all()
    serializer_class = serializers.GPUBaseboardTemplateSerializer
    table_class = tables.GPUBaseboardTemplateTable


class HBATemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for HBATemplate model."""

    bulk_create_form_class = forms.HBATemplateCSVForm
    bulk_update_form_class = forms.HBATemplateBulkEditForm
    create_form_class = forms.HBATemplateCreateForm
    filterset_class = filters.HBATemplateFilterSet
    form_class = forms.HBATemplateForm
    lookup_field = "pk"
    queryset = models.HBATemplate.objects.all()
    serializer_class = serializers.HBATemplateSerializer
    table_class = tables.HBATemplateTable


class MainboardTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for MainboardTemplate model."""

    bulk_create_form_class = forms.MainboardTemplateCSVForm
    bulk_update_form_class = forms.MainboardTemplateBulkEditForm
    create_form_class = forms.MainboardTemplateCreateForm
    filterset_class = filters.MainboardTemplateFilterSet
    form_class = forms.MainboardTemplateForm
    lookup_field = "pk"
    queryset = models.MainboardTemplate.objects.all()
    serializer_class = serializers.MainboardTemplateSerializer
    table_class = tables.MainboardTemplateTable


class NICTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for NICTemplate model."""

    bulk_create_form_class = forms.NICTemplateCSVForm
    bulk_update_form_class = forms.NICTemplateBulkEditForm
    create_form_class = forms.NICTemplateCreateForm
    filterset_class = filters.NICTemplateFilterSet
    form_class = forms.NICTemplateForm
    lookup_field = "pk"
    queryset = models.NICTemplate.objects.all()
    serializer_class = serializers.NICTemplateSerializer
    table_class = tables.NICTemplateTable


class OtherFSUTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for OtherFSUTemplate model."""

    bulk_create_form_class = forms.OtherFSUTemplateCSVForm
    bulk_update_form_class = forms.OtherFSUTemplateBulkEditForm
    create_form_class = forms.OtherFSUTemplateCreateForm
    filterset_class = filters.OtherFSUTemplateFilterSet
    form_class = forms.OtherFSUTemplateForm
    lookup_field = "pk"
    queryset = models.OtherFSUTemplate.objects.all()
    serializer_class = serializers.OtherFSUTemplateSerializer
    table_class = tables.OtherFSUTemplateTable


class PSUTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for PSUTemplate model."""

    bulk_create_form_class = forms.PSUTemplateCSVForm
    bulk_update_form_class = forms.PSUTemplateBulkEditForm
    create_form_class = forms.PSUTemplateCreateForm
    filterset_class = filters.PSUTemplateFilterSet
    form_class = forms.PSUTemplateForm
    lookup_field = "pk"
    queryset = models.PSUTemplate.objects.all()
    serializer_class = serializers.PSUTemplateSerializer
    table_class = tables.PSUTemplateTable


class RAMModuleTemplateUIViewSet(FSUTemplateModelViewSet):
    """View set for RAMModuleTemplate model."""

    bulk_create_form_class = forms.RAMModuleTemplateCSVForm
    bulk_update_form_class = forms.RAMModuleTemplateBulkEditForm
    create_form_class = forms.RAMModuleTemplateCreateForm
    filterset_class = filters.RAMModuleTemplateFilterSet
    form_class = forms.RAMModuleTemplateForm
    lookup_field = "pk"
    queryset = models.RAMModuleTemplate.objects.all()
    serializer_class = serializers.RAMModuleTemplateSerializer
    table_class = tables.RAMModuleTemplateTable
