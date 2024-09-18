Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a CPU Type represents a discrete model of a CPU, as defined by the Manufacturer, Name, and Part Number.
CPU Types are instantiated as CPUs installed within Devices, or as available spares in a Location.
For example, you may define a CPU Type for an **Intel Xeon Platinum 8570**, part number **PK8072205512100**.
CPU Types also have fields to track their Architecture (arm, X86, or other), their speed in MHz, and their number of cores.
Multiple instances of the CPU Type, named `cpu_0`, `cpu_1`, etc., can then be created as CPUs installed in a particular Device.
