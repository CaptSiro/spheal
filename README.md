# spheal
Simple script to manage project paths

```txt
Usage: /path/spheal.py <commands>
	select <slot> <path_id>
		Writes path of given <path_id> to specified <slot>. The destination of slot is determined by setting 'slots' + <slot>

	add <path> [, --slot=<slot_name>]
		Saves given path. If the optional argument --slot=<slot_name> is provided, it automatically selects the added path to <slot_name>

	delete <id> [, --pattern=<pattern>, --slot=<slot>]
		Deletes path with given entry. Use command `ls` to see ids for all saved paths. Use optional arguments to specify path. <pattern> must return specify only one path.

	ls [, <pattern>]
		Lists all saved paths. Use optional parameter <pattern> to search in saved paths

	setting <name> <value>
		Set <value> to <name>. Writeable settings are: 'slots'
```