A template for an HBA instance that will be created on all instantiations of the parent device type.
Each HBA template instance is assigned a physical [HBA Type](hbatype.md), a name, and a description (optional).
The name and PCI slot ID fields both support alphanumeric ranges for bulk creation, for example, setting the name to `hba_[0-4]` will create 5 HBA template instances with the digits in the name incremented from 0 to 4.
If a range is supplied for the PCI slot ID field as well, the number of generated labels must match the number of generated names.
