# v3.0 Release Notes

## [3.0.2 (2024-12-05)](https://github.com/NVIDIA/nautobot-app-fsus/releases/tag/v3.0.2)

### Fix

- FSUs and FSU types are now available in GraphQL queries ([#25](https://github.com/NVIDIA/nautobot-app-fsus/issues/25)).
- Add form guardrails for the parent device or location selection when editing or creating an FSU ([#26](https://github.com/NVIDIA/nautobot-app-fsus/issues/26)).
  - Changing the selected parent type will clear the other field, if set.
  - Status field options are updated based on the parent type, Active only valid when parent is a Device, Available only valid when parent is a Location.
- Fixed the breadcrumb display in the FSU model detail template.

### Miscellaneous

- Removed the workaround for the broken LinkedCountColumn in Nautobot versions 2.3.0 - 2.3.2.
- Updated minimum Nautobot version to 2.3.3.

## [3.0.1 (2024-10-10)](https://github.com/NVIDIA/nautobot-app-fsus/releases/tag/v3.0.1)

### Fix

- Set correct query parameter to filter parent FSUs by device when adding/updating a CPU, Disk, or GPU.

## [3.0.0 (2024-09-25)](https://github.com/NVIDIA/nautobot-app-fsus/releases/tag/v3.0.0)

### Overview

- Initial release compatible with Nautobot 2.3.0
