Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a RAM Module Type represents a discrete model of a memory module, as defined by the Manufacturer, Name, Part Number, Module Type (e.g. UDIMM), Technology (e.g. DDR5), Speed, Capacity, and Quantity.
RAM Module Types are instantiated as memory installed within Devices, or as available spares in a Location.
For example, you may define a RAM Module Type for a **Crucial - DDR5 - kit - 48 GB**, part number **CP2K24G60C48U5**.
Multiple instances of the RAM Module Type, named `dimm_0`, `dimm_1`, etc., can then be created as RAM Modules installed in a particular Device.
