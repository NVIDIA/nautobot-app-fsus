Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), an HBA Type represents a discrete model of an HBA, as defined by the Manufacturer, Name, and Part Number.
HBA Types are instantiated as HBAs installed within Devices, or as available spares in a Location.
For example, you may define an HBA Type for an **Supermicro - storage controller (RAID) - SAS 12Gb/s - PCIe 3.0 x8**, part number **AOC-SAS3-9380-8E**.
Multiple instances of the HBA Type, named `hba_0`, `hba_1`, etc., can then be created as HBAs installed in a particular Device.
