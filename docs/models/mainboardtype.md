Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a Mainboard Type represents a discrete model of a mainboard, as defined by the Manufacturer, Name, and Part Number.
Mainboard Types are instantiated as Mainboards installed within Devices, or as available spares in a Location.
For example, you may define a Mainboard Type for a **Supermicro X13SRA-TF Mainboard**, part number **MBD-X13SRA-TF-O**.
Mainboard Types also have fields to track their PCIe generation, and the number of CPU sockets they provide.
Instances of the Mainboard Type can then be created as Mainboards installed in a particular Devices.
