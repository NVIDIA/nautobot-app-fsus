Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a GPU Baseboard Type represents a discrete model of a storage device, as defined by the Manufacturer, Name, Part Number, and number of slots (optional).
GPU Baseboard Types are instantiated as GPU Baseboards installed within Devices, or as available spares in a Location.
For example, you may define a GPU Baseboard Type for a **DGX H100 Baseboard**, part number **x1024**.
Multiple instances of the GPU Baseboard Type, named `basebaord_0`, `baseboard_1`, etc., can then be created as GPU Baseboards available in storage, or installed in a particular Device.
