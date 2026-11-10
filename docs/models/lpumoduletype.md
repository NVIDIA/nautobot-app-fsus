Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), an LPU Module Type represents a discrete model of a circuit board containing one or more Language Processing Unit (LPU) inference-accelerator ASICs, as defined by the Manufacturer, Name, Part Number, and LPU Count.
The LPU architecture is based on technology licensed by NVIDIA from Groq.
LPU Module Types are instantiated as accelerator boards installed within Devices, or as available spares in a Location.
For example, you may define an LPU Module Type for an **NVIDIA Groq 3 LPU Module** containing one **LP30 LPU**.
Multiple instances of the LPU Module Type, named `lpu_module_0`, `lpu_module_1`, etc., can then be created as LPU Modules installed in a particular Device.
