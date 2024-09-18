Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a Disk Type represents a discrete model of a storage device, as defined by the Manufacturer, Name, Part Number, Type (HDD, SDD, NVME), and Size (optional).
Disk Types are instantiated as Disks installed within Devices, or as available spares in a Location.
For example, you may define a Disk Type for a **Seagate FireCuda 530 2TB NVME SSD**, part number **ZP2000GM3A013**.
Multiple instances of the Disk Type, named `nvme_0`, `nvme_1`, etc., can then be created as Disks installed in a particular Device.
