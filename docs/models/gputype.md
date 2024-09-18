Similar to a [Nautobot Device Type](/static/docs/models/dcim/devicetype.html), a GPU Type represents a discrete model of a GPU, as defined by the Manufacturer, Name, and Part Number.
GPU Types are instantiated as GPUs installed within Devices, or as available spares in a Location.
For example, you may define a GPU Type for an **NVIDIA H100 Tensor Core GPU**, part number **699-21010-0200-xxx**.
Multiple instances of the GPU Type, named `gpu_0`, `gpu_1`, etc., can then be created as GPUs installed in a particular Device.
