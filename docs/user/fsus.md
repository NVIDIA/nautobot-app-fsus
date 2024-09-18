Field Serviceable Units are tracked assets that are not independent Devices, but may be installed in a [Device](/static/docs/models/dcim/device.html) or a spare in a storage [Location](/static/docs/models/dcim/location.html).

There are ten FSU types available - CPU, Disk, Fan, GPU, GPU Baseboard, HBA, Mainboard, NIC, PSU, and RAM Module.

!!! info
    The types listed above are supported directly as distinct FSUs, for other FSUs to be tracked there is an OtherFSU type.

## FSU vs FSU Type vs FSU Template

Field Serviceable Units (FSUs) are made up of two models (FSU and FSU type), with a third (FSU template) that allows FSUs to be assigned to a [DeviceType](/static/docs/models/dcim/devicetype.html) and created automatically with Devices based on that DeviceType.

### FSU Type

Similar to a Nautobot [DeviceType](/static/docs/models/dcim/devicetype.md), an FSU type represents the individual FSU product, defined by the manufacturer, name, and part number.
For example, a GPUType may be:

- Manufacturer: NVIDIA
- Name: H100 Tensor Core GPU
- Part Number: 699-21010-0200-xxx.

Some FSU types have additional product-specific fields:

- CPU type has fields for architecture, clock speed, number of cores, and the PCIe generation.
- Disk type has fields for the type of disk, e.g. NVME, and the size.
- GPU Baseboard type has a field for the number of GPU slots provided.
- Mainboard type has a field for the number of CPU sockets provided.
- NIC type has a field for the number of interfaces provided.
- PSU type has fields for the feed type (AC, DC, or Switchable), the power provided in Watts, the required voltage (e.g. `-40V - -72` for DC or `100-240V` for AC), and whether the unit is hot-swappable.
- RAM Module type has fields for the module type, e.g. UDIMM, the memory technology, e.g. DDR5, memory speed in MHz, memory size in GB, and the number of modules that are included in the part number.

### FSU

A Field Serviceable Unit is a physical asset based on an FSU type being tracked in inventory.
An FSU must be associated with either a storage location or a parent device, and each FSU in a storage location or device must have a unique name.
Each FSU can also be assigned an asset tag, and a description.
Common FSU state data items are serial number, firmware version, driver name, and driver version.

Some FSUs have additional options:

- CPUs can be connected to a parent Mainboard.
- Disks can connected to a parent HBA.
- GPUs have a field for their PCI slot ID, and can be connected to a parent GPU Baseboard.
- HBAs have a field for their PCI slot ID.
- NICs have a field for their PCI slot ID, and can be connected to the Device [Interface](/static/docs/models/dcim/interface.html) components that they provide.
- PSUs can be set as redundant, and can be connected to the Device [Power Port](/static/docs/models/dcim/powerport.html) components that they provide.
- RAM Modules have a field for their memory slot ID.

### FSU Template

Similar to Nautobot's [component templates](/static/docs/core-functionality/device-types.html#device-component-templates), FSU templates represent the FSU assets that are present in a particular DeviceType.
They are added to a DeviceType, and when a new Device is added to the inventory based on a DeviceType with FSU templates, the FSUs for the Device are created automatically.

FSU templates can be added by using the **Add FSUs** menu on the details page of a DeviceType.
The Name field supports alphanumeric ranges, so multiple FSUs can be added to a DeviceType at once.
PCI slot ID fields, and the RAM Module memory slot ID field, also support alphanumeric ranges.

## Filter Extensions

The FSUs app extends the filter sets for Devices, Locations, Interfaces, and Power Ports in Nautobot to allow filtering those objects on their associated FSUs.

### Devices and Locations

Devices and Locations can be filtered based on the presence of FSUs.
In the UI, the filter is available under the Advanced tab when configuring filtering.
Set the filter field to the FSU you would like to filter on, e.g. **Has GPUs**, and the lookup type to **is null**.
You can then select either **Yes** or **No** to filter for devices/locations that either have or do not have the chosen FSU.

The filter can also be used by attaching a query parameter to the request URL for the device or location lists.
The parameters for filtering by FSUs on devices are:

- `device_has_cpus`
- `device_has_disks`
- `device_has_fans`
- `device_has_gpus`
- `device_has_gpubaseboards`
- `device_has_hbas`
- `device_has_mainboards`
- `device_has_nics`
- `device_has_otherfsus`
- `device_has_psus`
- `device_has_rammodules`

For locations they are:

- `location_has_available_cpus`
- `location_has_available_disks`
- `location_has_available_fans`
- `location_has_available_gpus`
- `location_has_available_gpubaseboards`
- `location_has_available_hbas`
- `location_has_available_mainboards`
- `location_has_available_nics`
- `location_has_available_otherfsus`
- `location_has_available_psus`
- `location_has_available_rammodules`

Set the parameter value to either `True` or `False`.

```
http://nautobot.server/dcim/devices/?device_has_gpus=True
http://nautobot.server/dcim/locations/?location_has_available_gpus=True
```

### Interfaces

Device Interface components can be filtered either for those that have a parent NIC assigned, or those assigned to particular parent NICs.
As with Device and Location filters, these filter options are available under the Advanced tab as **Has a parent NIC** and **Parent NIC (Name or ID)**, and the request query parameters are:

- `interface_has_parent_nic`
- `interface_parent_nic`

As implied by the field name in the UI, the parent NIC filter matches on name or ID, so either can be used in a query parameter.

```
http://nautobot.server/dcim/interfaces/?interface_has_parent_nic=True
http://nautobot.server/dcim/interfaces/?interface_parent_nic=NIC_01
http://nautobot.server/dcim/interfaces/?interface_parent_nic=96999339-c462-4de2-96c4-751747d393b5
```

### Power Ports

Device power port components can be filtered either for those that have a parent PSU assigned, or those assigned to particular parent PSUs.
As with Interface filters, these filter options are available under the Advanced tab as **Has a parent PSU** and **Parent PSU (Name or ID)**, and the request query parameters are:

- `powerport_has_parent_psu`
- `powerport_parent_psu`

As implied by the field name in the UI, the parent PSU filter matches on name or ID, so either can be used in a query parameter.

```
http://nautobot.server/dcim/power-ports/?powerport_has_parent_psu=True
http://nautobot.server/dcim/power-ports/?powerport_parent_psu=psu_0
http://nautobot.server/dcim/power-ports/?powerport_parent_psu=3b318448-399a-4322-8719-408982bc2fe3
```

## Filtering

### CPUs

CPUs can be filtered either for those tha have a parent Mainboard, or those that have a specific parent Mainboard.
These filter options are available under the Advanced tab as **Has a parent Mainboard** and **Parent Mainboard (Name or ID)**, and the request parameters are:

- `has_parent_mainboard`
- `parent_mainboard`

### Disks

Disks can be filtered either for those tha have a parent HBA, or those that have a specific parent HBA.
These filter options are available under the Advanced tab as **Has a parent HBA** and **Parent HBA (Name or ID)**, and the request parameters are:

- `has_parent_hba`
- `parent_hba`

### GPUs

GPUs can be filtered either for those that have a parent GPU Baseboard, or those that have a specific parent GPU Baseboard.
These filter options are available under the Advanced tab as **Has a parent GPU Baseboard** and **Parent GPU Baseboard (Name or ID)**, and the request parameters are:

- `has_parent_baseboard`
- `parent_baseboard`

### GPU Baseboards

GPU Baseboards can be filtered for those that have child GPUs associated with them.
The filter option is available under the Advanced tab as **Has Child GPUs**, and the request parameter is:

- `has_child_gpus`

### HBAs

HBAs can be filtered for those that have child Disks associated with them.
The filter option is available under the Advanced tab as **Has Child Disks**, and the request parameter is:

- `has_child_disks`

### Mainboards

Mainboards can be filtered for those that have child CPUs associated with them.
The filter option is available under the Advanced tab as **Has Child CPUs**, and the request parameter is:

- `has_child_cpus`

### NICs

NICs can be filtered for those that have child Interfaces associated with them.
The filter option is available under the Advanced tab as **Has Child Interfaces**, and the request parameter is:

- `has_child_interfaces`

### PSUs

PSUs can be filtered for those that have child Power Ports associated with them.
The filter option is available under the Advanced tab as **Has Child Power Ports**, and the request parameter is:

- `has_child_power_ports`
