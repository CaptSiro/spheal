# spheal
Simple script to manage project paths

- `program [, help]`
  - Shows this help
- `program add <path> [, --slot=<slot>]`
  - Adds path, but it is not selected
  - You can specify slot for this path with the `--slot=<slot>` argument
- `program delete <id>`
  - Deletes path with given entry. Use command `ls` to see ids for all saved paths
- `program ls [, pattern]`
  - Lists all saved paths. Use optional parameter pattern to search in saved paths
- `program set <setting> <value>`
  - Sets value of specified setting
  - Writeable settings:
    - `slots` - Absolute file path that will be used to store slots. File example: `~/spheal-slot-` Directory example: `~/spheal-slots/`
