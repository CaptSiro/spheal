# spheal
Simple script to manage project paths

- `program [, help]`
  - Shows this help
- `program add path`
  - Adds path, but it is not selected
- `program delete id`
  - Deletes path with given entry. Use command `ls` to see ids for all saved paths
- `program ls [, pattern]`
  - Lists all saved paths in `[id] path` format. Use optional parameter pattern to search in saved paths
- `program set setting value`
  - Sets value of specified setting
  - Writeable settings: `slots`
