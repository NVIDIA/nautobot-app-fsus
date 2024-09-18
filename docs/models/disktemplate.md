A template for a Disk instance that will be created on all instantiations of the parent device type.
Each Disk template instance is assigned a physical [Disk Type](disktype.md), a name, and a description (optional).
The name field supports alphanumeric ranges for bulk creation, for example, setting the name to `nvme_[0-4]` will create 5 Disk template instances with the digits in the name incremented from 0 to 4.
