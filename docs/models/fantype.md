Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a Fan Type represents a discrete model of a cooling fan, as defined by the Manufacturer, Name, and Part Number.
Fan Types are instantiated as Fans installed within Devices, or as available spares in a Location.
For example, you may define a Fan Type for a **HPE Standard 1U Fan**, part number **P54697-B21**.
Multiple instances of the Fan Type, named `fan_0`, `fan_1`, etc., can then be created as Fans installed in a particular Device.
