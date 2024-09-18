Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a NIC Type represents a discrete model of a NIC, as defined by the Manufacturer, Name, and Part Number.
NIC Types are instantiated as NICs installed within Devices, or as available spares in a Location.
For example, you may define a NIC Type for an **NVIDIA ConnectX-6 VPI Adapter Card HDR/200GbE**, part number **MCX653106A-HDAT-SP**.
Multiple instances of the NIC Type, named `nic_0`, `nic_1`, etc., can then be created as NICs installed in a particular Device.
