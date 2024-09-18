Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a PSU Type represents a discrete model of a power supply unit, as defined by the Manufacturer, Name, Part Number, Power Feed Type, Supplied Watts (optional), Required Voltage (optional), and whether the unit is hot-swappable.
PSU Types are instantiated as PSUs installed within Devices, or as available spares in a Location.
For example, you may define a PSU Type for an **NVIDIA 550W AC Power Supply**, part number **MTEF-PSF-AC-I**, with an input voltage of **100-240V**.
Multiple instances of the PSU Type, named `PSU 0`, `PSU 1`, etc., can then be created as PSUs installed in a particular Device.
