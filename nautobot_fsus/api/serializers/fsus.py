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

"""Model serializers for FSU API endpoints."""
from copy import copy
from typing import Any

from nautobot.dcim.models import Interface, PowerPort
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from nautobot_fsus.api.mixins import FSUModelSerializer
from nautobot_fsus.api.nested_serializers import (
    NestedCPUTypeSerializer,
    NestedDiskTypeSerializer,
    NestedFanTypeSerializer,
    NestedGPUBaseboardSerializer,
    NestedGPUBaseboardTypeSerializer,
    NestedGPUTypeSerializer,
    NestedHBASerializer,
    NestedHBATypeSerializer,
    NestedMainboardSerializer,
    NestedMainboardTypeSerializer,
    NestedNICTypeSerializer,
    NestedOtherFSUTypeSerializer,
    NestedPSUTypeSerializer,
    NestedRAMModuleTypeSerializer,
)
from nautobot_fsus.models import (
    CPU,
    Disk,
    Fan,
    GPUBaseboard,
    GPU,
    HBA,
    Mainboard,
    NIC,
    OtherFSU,
    PSU,
    RAMModule,
)


class CPUSerializer(FSUModelSerializer):
    """API serializer for CPU model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:cpu-detail")
    parent_mainboard = NestedMainboardSerializer(required=False, allow_null=True)
    fsu_type = NestedCPUTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """CPUserializer model options."""

        model = CPU
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "parent_mainboard",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
        ]

    def validate_sockets(self, mainboard: Mainboard):
        """Validate that the parent Mainboard has available sockets."""
        if mainboard.fsu_type.cpu_socket_count and mainboard.fsu_type.cpu_socket_count > 0:
            if mainboard.cpus.count() >= mainboard.fsu_type.cpu_socket_count:
                raise serializers.ValidationError(
                    {
                        "parent_mainboard": "Mainboard has no available CPU sockets."
                    }
                )

    def create(self, validated_data: Any) -> CPU:
        """Create a new CPU instance with parent Mainboard validation."""
        instance = CPU(**validated_data)
        if instance.parent_mainboard is not None:
            self.validate_parent_device(
                [instance],
                instance.parent_mainboard.device,  # pylint: disable=no-member
                "parent_mainboard",
            )

            self.validate_sockets(instance.parent_mainboard)

        instance.validated_save()
        return instance

    def update(self, instance: CPU, validated_data: Any) -> CPU:
        """Update an existing CPU instance with parent Mainboard validation."""
        # For update operations we need to know if the parent_mainboard field is present in the
        # PUT/PATCH data, if it is explicitly set to null it triggers clearing the value
        mainboard = validated_data.get("parent_mainboard", False)
        if mainboard and mainboard is not None:
            if instance.parent_mainboard != mainboard:
                # Mainboard is changing, validate parent Device and available sockets
                self.validate_parent_device([instance], mainboard.device, "parent_mainboard")
                self.validate_sockets(mainboard)

        validated_instance: CPU = super().update(instance, validated_data)
        return validated_instance


class DiskSerializer(FSUModelSerializer):
    """API serializer for Disk model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:disk-detail")
    parent_hba = NestedHBASerializer(required=False, allow_null=True)
    fsu_type = NestedDiskTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """DiskSerializer model options."""

        model = Disk
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "parent_hba",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
        ]

    def create(self, validated_data: Any) -> Disk:
        """Create a new Disk instance with parent HBA validation."""
        instance = Disk(**validated_data)
        if instance.parent_hba is not None:
            self.validate_parent_device(
                [instance],
                instance.parent_hba.device,  # pylint: disable=no-member
                "parent_hba",
            )

        instance.validated_save()
        return instance

    def update(self, instance: Disk, validated_data: Any) -> Disk:
        """Update an existing Disk instance with parent HBA validation."""
        # For update operations we need to know if the parent_mainboard field is present in the
        # PUT/PATCH data, if it is explicitly set to null it triggers clearing the value
        hba = validated_data.get("parent_hba", False)
        if hba and hba is not None:
            if instance.parent_hba != hba:
                # HBA is changing, validate parent Device
                self.validate_parent_device([instance], hba.device, "parent_hba")

        validated_instance: Disk = super().update(instance, validated_data)
        return validated_instance


class FanSerializer(FSUModelSerializer):
    """API serializer for Fan model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:fan-detail")
    fsu_type = NestedFanTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """FanSerializer model options."""

        model = Fan


class GPUBaseboardSerializer(FSUModelSerializer):
    """API serializer for GPUBaseboard model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gpubaseboard-detail")
    fsu_type = NestedGPUBaseboardTypeSerializer()
    gpus = serializers.PrimaryKeyRelatedField(
        queryset=GPU.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta(FSUModelSerializer.Meta):
        """GPUBaseboardSerializer model options."""

        model = GPUBaseboard
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "gpus",
            "description",
        ]

    def validate(self, data: Any):
        """Need to hide the gpus field from normal validation."""
        to_validate = copy(data)

        # Need to remove the list of gpus before the first validation step, otherwise the
        # model validation will complain because you can't set parent_gpubaseboard on the gpus in
        # this direction, that's handled in the create()/update() methods.
        _ = to_validate.pop("gpus", None)

        super().validate(to_validate)

        return data

    def create(self, validated_data: Any) -> GPUBaseboard:
        """Create a new GPUBaseboard instance with child GPU validation."""
        # gpus is optional in the POST data, set it to an empty list if it's not present.
        gpus = validated_data.pop("gpus", [])

        if gpus:
            # Validate parent device
            self.validate_parent_device(gpus, validated_data.get("device", None), "gpus")

            # Validate available slots
            baseboard_type = validated_data["fsu_type"]
            if baseboard_type.slot_count is not None and len(gpus) > baseboard_type.slot_count:
                raise serializers.ValidationError(
                    {
                        "gpus": f"Number of GPUs being added to Baseboard ({len(gpus)}) is "
                                f"greater than the number of available slots "
                                f"({baseboard_type.slot_count})"
                    }
                )

            # Child GPUs must not have a parent GPU Baseboard assigned
            for gpu in gpus:
                if gpu.parent_gpubaseboard is not None:
                    raise serializers.ValidationError(
                        {
                            "gpus": f"GPU {gpu.name} is already assigned "
                                    f"to {gpu.parent_gpubaseboard.name}"
                        }
                    )

        # Create the GPUBaseboard instance
        instance = GPUBaseboard.objects.create(**validated_data)

        # Set parent_gpubaseboard for any specified child GPU instances
        for gpu in gpus:
            gpu.parent_gpubaseboard = instance
            gpu.validated_save()

        return instance

    def update(self, instance: GPUBaseboard, validated_data: Any) -> GPUBaseboard:
        """
        Update an existing GPUBaseboard instance.

        PUT requests must have all required field, PATCH requests need only the changed fields.
        When updating a GPUBaseboard instance, child GPUs update logic is:
        - gpus not set or null, device and storage location not updated -> no changes
        - gpus set and device is not set or instance device is None -> ValidationError
        - gpus is an empty list -> clear parent_gpubaseboard on any existing child GPUs
        - gpus is set, device is set or instance.device is not None and any gpu.device is not
            the same as the device value or the instance.device -> ValidationError
        - gpus is set, device is set or instance.device is not None -> set parent_gpubaseboard to
            instance for GPUs in the list, clear parent_gpubaseboard for any that are currently set
            to the instance but are not in the list
        - gpus not set or null and storage location set -> clear any existing child GPUs
        """
        # For update operations we need to know if the gpus field is present in the PUT/PATCH data,
        # as an empty list triggers clearing parent_gpubaseboard for current child GPUs
        gpus = validated_data.pop("gpus", None)

        location = validated_data.get("location", None)
        parent_device = None if location else validated_data.get("device", instance.device)

        if gpus is not None:
            # An empty list means we're clearing the child GPUs for this GPUBasebaord
            if len(gpus) == 0:
                for gpu in instance.gpus.all():
                    gpu.parent_gpubaseboard = None
                    gpu.validated_save()

            # Validate and update the child GPUs to the new list
            else:
                # Validate the parent device
                self.validate_parent_device(gpus, parent_device, "gpus")

                # Validate available slots
                baseboard_type = instance.fsu_type
                if (baseboard_type.slot_count is not None
                        and len(gpus) > int(baseboard_type.slot_count)):
                    raise serializers.ValidationError(
                        {
                            "gpus": f"Number of GPUs being added to Baseboard ({len(gpus)}) is "
                                    f"greater than the number of available slots "
                                    f"({baseboard_type.slot_count})"
                        }
                    )

                # Track the currently set child GPUs to update properly if the list has changed
                current_gpus = set(list(instance.gpus.all()))
                new_gpus = set()
                for gpu in gpus:
                    # New child GPUs must not have a parent GPUBaseboard assigned
                    if gpu not in current_gpus and gpu.parent_gpubaseboard is not None:
                        raise serializers.ValidationError(
                            {
                                "gpus": f"GPU {gpu.name} is already assigned "
                                        f"to {gpu.parent_gpubaseboard.name}"
                            }
                        )
                    new_gpus.add(gpu)

                # Set parent_gpubaseboard for newly added child GPUs
                for new_gpu in new_gpus.difference(current_gpus):
                    new_gpu.parent_gpubaseboard = instance
                    new_gpu.validated_save()

                # Remove any currently assigned child GPUs that are not in the updated list
                for gpu in current_gpus.difference(new_gpus):
                    gpu.parent_gpubaseboard = None
                    gpu.validated_save()

        # Moving a GPUBaseboard to a location means we need to clear any child GPUs
        elif location is not None:
            for gpu in instance.gpus.all():
                gpu.parent_gpubaseboard = None
                gpu.validated_save()

        validated_instance: GPUBaseboard = super().update(instance, validated_data)
        return validated_instance


class GPUSerializer(FSUModelSerializer):
    """API serializer for GPU model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:gpu-detail")
    parent_gpubaseboard = NestedGPUBaseboardSerializer(required=False, allow_null=True)
    fsu_type = NestedGPUTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """GPUSerializer model options."""

        model = GPU
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "parent_gpubaseboard",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
        ]

    def validate_slots(self, baseboard: GPUBaseboard):
        """Validate that the parent GPUBaseboard has available slots."""
        if baseboard.fsu_type.slot_count and int(baseboard.fsu_type.slot_count) > 0:
            if baseboard.gpus.count() >= baseboard.fsu_type.slot_count:
                raise serializers.ValidationError(
                    {
                        "parent_gpubaseboard": "GPU Baseboard has no available GPU slots"
                    }
                )

    def create(self, validated_data: Any) -> GPU:
        """Create a new GPU instance with parent GPUBaseboard validation."""
        instance = GPU(**validated_data)
        if instance.parent_gpubaseboard is not None:
            self.validate_parent_device(
                [instance],
                instance.parent_gpubaseboard.device,  # pylint: disable=no-member
                "parent_gpubaseboard",
            )

            self.validate_slots(instance.parent_gpubaseboard)

        instance.validated_save()
        return instance

    def update(self, instance: GPU, validated_data: Any) -> GPU:
        """Update an existing GPU instance with parent GPUBaseboard validation."""
        # For update operations we need to know if the parent_gpubaseboard field is present in the
        # PUT/PATCH data, if it is explicitly set to null it triggers clearing the value
        baseboard = validated_data.get("parent_gpubaseboard", False)
        if baseboard and baseboard is not None:
            if instance.parent_gpubaseboard != baseboard:
                # GPUBaseboard is changing, validate parent Device and available slots
                self.validate_parent_device([instance], baseboard.device, "parent_gpubaseboard")
                self.validate_slots(baseboard)

        validated_instance: GPU = super().update(instance, validated_data)
        return validated_instance


class HBASerializer(FSUModelSerializer):
    """API serializer for HBA model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:hba-detail")
    fsu_type = NestedHBATypeSerializer()
    disks = serializers.PrimaryKeyRelatedField(
        queryset=Disk.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta(FSUModelSerializer.Meta):
        """HBASerializer model options."""

        model = HBA
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "disks",
            "description",
        ]

    def validate(self, data: Any):
        """Need to hide the disks field from normal validation."""
        to_validate = copy(data)

        # Need to remove the list of disks before the first validation step, otherwise the
        # model validation will complain because you can't set parent_hba on the disks in
        # this direction, that's handled in the create()/update() methods.
        _ = to_validate.pop("disks", None)

        super().validate(to_validate)

        return data

    def create(self, validated_data: Any) -> HBA:
        """Create a new HBA instance with child Disk validation."""
        # disks is optional in the POST data, set it to an empty list if it's not present
        disks = validated_data.pop("disks", [])

        if disks:
            # Validate parent device
            self.validate_parent_device(disks, validated_data.get("device", None), "disks")

            # Child disks must not have a parent HBA assigned
            for disk in disks:
                if disk.parent_hba is not None:
                    raise serializers.ValidationError(
                        {
                            "disks": f"Disk {disk.name} is already assigned "
                                     f"to {disk.parent_hba.name}"
                        }
                    )

        # Create the HBA instance
        instance = HBA.objects.create(**validated_data)

        # Set the parent_hba for any specified child Disk instances
        for disk in disks:
            disk.parent_hba = instance
            disk.validated_save()

        return instance

    def update(self, instance: HBA, validated_data: Any) -> HBA:
        """
        Update an existing HBA instance.

        PUT requests must have all required field, PATCH requests need only the changed fields.
        When updating an HBA instance, child Disks update logic is:
        - disks not set or null, device and storage location not updated -> no changes
        - disks set and device is not set or instance device is None -> ValidationError
        - disks is an empty list -> clear parent_hba on any existing child Disks
        - disks is set, device is set or instance.device is not None and any disk.device is not
            the same as the device value or the instance.device -> ValidationError
        - disks is set, device is set or instance.device is not None -> set parent_hba to
            instance for Disks in the list, clear parent_hba for any that are currently set
            to the instance but are not in the list
        - disks not set or null and storage location set -> clear any existing child Disks
        """
        # For update operations we need to know if the disks field is present in the PUT/PATCH data,
        # as an empty list triggers clearing parent_gpubaseboard for current child Disks
        disks = validated_data.pop("disks", None)

        location = validated_data.get("location", None)
        parent_device = None if location else validated_data.get("device", instance.device)

        if disks is not None:
            # An empty list means we're clearing the child Disks for this HBA
            if len(disks) == 0:
                for disk in instance.disks.all():
                    disk.parent_hba = None
                    disk.validated_save()

            # Validate and update the child Disks to the new list
            else:
                # Validate the parent device
                self.validate_parent_device(disks, parent_device, "disks")

                # Track the currently set child Disks to update properly if the list has changed
                current_disks = list(instance.disks.all())
                new_disks = []
                for disk in disks:
                    if disk in current_disks:
                        current_disks.remove(disk)
                    # New child Disks must not have a parent HBA assigned
                    elif disk.parent_hba is not None:
                        raise serializers.ValidationError(
                            {
                                "disks": f"Disk {disk.name} is already assigned "
                                         f"to {disk.parent_hba.name}"
                            }
                        )
                    else:
                        new_disks.append(disk)

                # Set parent_hba for newly added child Disks
                for new_disk in new_disks:
                    new_disk.parent_hba = instance
                    new_disk.validated_save()

                # Remove any currently assigned child Disks that are not in the updated list
                for disk in current_disks:
                    disk.parent_hba = None
                    disk.validated_save()

        # Moving an HBA to a location means we need to clear any child Disks
        elif location is not None:
            for disk in instance.disks.all():
                disk.parent_hba = None
                disk.validated_save()

        validated_instance: HBA = super().update(instance, validated_data)
        return validated_instance


class MainboardSerializer(FSUModelSerializer):
    """API serializer for Mainboard model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:mainboard-detail")
    fsu_type = NestedMainboardTypeSerializer()
    cpus = serializers.PrimaryKeyRelatedField(
        queryset=CPU.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta(FSUModelSerializer.Meta):
        """MainboardSerializer model options."""

        model = Mainboard
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "cpus",
            "description",
        ]

    def validate(self, data: Any):
        """Need to hide the cpus field from normal validation."""
        to_validate = copy(data)

        # Need to remove the list of cpus before the first validation step, otherwise the
        # model validation will complain because you can't set parent_mainboard on the cpus in
        # this direction, that's handled in the create()/update() methods.
        _ = to_validate.pop("cpus", None)

        super().validate(to_validate)

        return data

    def create(self, validated_data: Any) -> Mainboard:
        """Create a new Mainboard instance with child CPU validation."""
        # cpus is optional in the POST data, set it to an empty list if it's not present.
        cpus = validated_data.pop("cpus", [])

        if cpus:
            # Validate parent device
            self.validate_parent_device(cpus, validated_data.get("device", None), "cpus")

            # Validate available sockets
            mainboard_type = validated_data["fsu_type"]
            if (mainboard_type.cpu_socket_count is not None
                    and len(cpus) > mainboard_type.cpu_socket_count):
                raise serializers.ValidationError(
                    {
                        "cpus": f"Number of CPUs being added to Mainboard ({len(cpus)}) is "
                                f"greater than the number of available sockets "
                                f"({mainboard_type.cpu_socket_count})"
                    }
                )

            # Child CPUs must not have a parent Mainboard assigned
            for cpu in cpus:
                if cpu.parent_mainboard is not None:
                    raise serializers.ValidationError(
                        {
                            "cpus": f"CPU {cpu.name} is already assigned "
                                    f"to {cpu.parent_mainboard.name}"
                        }
                    )

        # Create the Mainboard instance
        instance = Mainboard.objects.create(**validated_data)

        # Set parent_mainboard for any specified child CPU instance
        for cpu in cpus:
            cpu.parent_mainboard = instance
            cpu.validated_save()

        return instance

    def update(self, instance: Mainboard, validated_data: Any) -> Mainboard:
        """
        Update an existing Mainboard instance.

        PUT requests must have all required field, PATCH requests need only the changed fields.
        When updating a Mainboard instance, child CPUs update logic is:
        - cpus not set or null, device and storage location not updated -> no changes
        - cpus set and device is not set or instance device is None -> ValidationError
        - cpus is an empty list -> clear parent_mainboard on any existing child CPUs
        - cpus is set, device is set or instance.device is not None and any cpu.device is not
            the same as the device value or the instance.device -> ValidationError
        - cpus is set, device is set or instance.device is not None -> set parent_mainboard to
            instance for CPUs in the list, clear parent_mainboard for any that are currently set
            to the instance but are not in the list
        - cpus not set or null and storage location set -> clear any existing child CPUs
        """
        # For update operations we need to know if the cpus field is present in the PUT/PATCH data,
        # as an empty list triggers clearing parent_mainboard for current child CPUs
        cpus = validated_data.pop("cpus", None)

        location = validated_data.get("location", None)
        parent_device = None if location else validated_data.get("device", instance.device)

        if cpus is not None:
            # An empty list means we're clearing the child CPUs for this Mainboard
            if len(cpus) == 0:
                for cpu in instance.cpus.all():
                    cpu.parent_mainboard = None
                    cpu.validated_save()

            # Validate and update the child CPUs to the new list
            else:
                # Validate the parent device
                self.validate_parent_device(cpus, parent_device, "cpus")

                # Validate available sockets
                mainboard_type = instance.fsu_type
                if (mainboard_type.cpu_socket_count is not None
                        and len(cpus) > mainboard_type.cpu_socket_count):
                    raise serializers.ValidationError(
                        {
                            "cpus": f"Number of CPUs being added to Mainboard ({len(cpus)}) is "
                                    f"greater than the number of available sockets "
                                    f"({mainboard_type.cpu_socket_count})"
                        }
                    )

                # Track the currently set child CPUs to update properly if the list has changed
                current_cpus = set(list(instance.cpus.all()))
                new_cpus = set()
                for cpu in cpus:
                    # New child CPU must not have a parent Mainboard assigned
                    if cpu not in current_cpus and cpu.parent_mainboard is not None:
                        raise serializers.ValidationError(
                            {
                                "cpus": f"CPU {cpu.name} is already assigned "
                                        f"to {cpu.parent_mainboard.name}"
                            }
                        )

                    new_cpus.add(cpu)

                # Set parent_mainboard for newly added child CPUs
                for new_cpu in new_cpus.difference(current_cpus):
                    new_cpu.parent_mainboard = instance
                    new_cpu.validated_save()

                # Remove any currently assigned child CPUs that are not in the updated list
                for cpu in current_cpus.difference(new_cpus):
                    cpu.parent_mainboard = None
                    cpu.validated_save()

        # Moving a Mainboard to a location means we need to clear any child CPUs
        elif location is not None:
            for cpu in instance.cpus.all():
                cpu.parent_mainboard = None
                cpu.validated_save()

        validated_instance: Mainboard = super().update(instance, validated_data)
        return validated_instance


class NICSerializer(FSUModelSerializer):
    """API serializer for NIC model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:nic-detail")
    fsu_type = NestedNICTypeSerializer()
    interfaces = serializers.PrimaryKeyRelatedField(
        queryset=Interface.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta(FSUModelSerializer.Meta):
        """NICSerializer model options."""

        model = NIC
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "interfaces",
            "description",
        ]


class OtherFSUSerializer(FSUModelSerializer):
    """API serializer for Other FSU model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:otherfsu-detail")
    fsu_type = NestedOtherFSUTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """OtherFSUSerializer model options."""

        model = OtherFSU


class PSUSerializer(FSUModelSerializer):
    """API serializer for PSU model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:psu-detail")
    fsu_type = NestedPSUTypeSerializer()
    power_ports = serializers.PrimaryKeyRelatedField(
        queryset=PowerPort.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta(FSUModelSerializer.Meta):
        """PSUSerializer model options."""

        model = PSU
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "power_ports",
            "description",
        ]


class RAMModuleSerializer(FSUModelSerializer):
    """API serializer for RAM Module model."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_fsus-api:rammodule-detail")
    fsu_type = NestedRAMModuleTypeSerializer()

    class Meta(FSUModelSerializer.Meta):
        """RAMModuleSerializer model options."""

        model = RAMModule
        fields = [
            "id",
            "url",
            "name",
            "device",
            "location",
            "fsu_type",
            "slot_id",
            "serial_number",
            "firmware_version",
            "driver_version",
            "driver_name",
            "asset_tag",
            "status",
            "description",
        ]
