# Field Serviceable Units for Nautobot

## Overview

Field Serviceable Units for Nautobot is an app that adds models for tracking hardware components that may be installed in a Device or kept as spares at a Location.
Included are models for CPUs, Disks, Fans, GPUs, GPU Baseboards, HBAs, Mainboards, NICs, PSUs, and RAM Modules, along with generic Other FSUs for tracking types not covered by the specific models.
Similar to Devices in Nautobot, an FSU is based on an FSU Type, which is the representation of the physical product - a manufacturer, name, and part number.
In addition, FSU Types track common elements of the specific FSU product, for example, a CPU type will have the architecture, clock speed, number of cores, and the PCIe generation.

### FSU Templates

Special template versions of FSU models are available to be assigned to Device Types.
These behave like the Component Templates in Nautobot, when a new Device is added based on a Device Type with assigned FSU Templates, the FSUs represented by the templates are created and assigned to the Device automatically.

## License

Field Serviceable Units for Nautobot is released under the Apache 2.0 license.

This project will download and install additional third-party open source software projects.
Review the license terms of these open source projects before use.
