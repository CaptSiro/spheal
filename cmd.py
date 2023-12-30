import conf
import os
import utils


class Args:
    def __init__(self, common, named):
        self.named = named
        self.common = common

    @staticmethod
    def parse(args) -> "Args":
        common = []
        named = {}

        for arg in args:
            a = str(arg)
            if a.startswith("--"):
                name, value = a.split("=", 1)
                named[str(name).replace("--", '')] = value
                continue

            common.append(a)

        return Args(common, named)



def command(arguments, description):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper.__dict__["is_command"] = True
        wrapper.arguments = arguments
        wrapper.description = description
        wrapper.command_name = str(fn.__name__).replace("cmd_", "")
        wrapper.__name__ = fn.__name__

        return wrapper
    return decorator

def is_cmd(obj):
    return hasattr(obj, "__dict__") and "is_command" in obj.__dict__



def select_slot(config, slot, path_id):
    i = utils.index_of(config["paths"], lambda p: str(p[0]) == str(path_id))
    if i is None:
        print(f"Could not find path with id `{path_id}`")
        return

    path = config["paths"][i]

    old = utils.index_of(config["paths"], lambda p: str(p[2]) == str(slot))
    if old is not None:
        os.unlink(config["slots"] + config["paths"][old][2])
        config["paths"][old][2] = "NULL"

    file_name = config["slots"] + str(slot)
    with open(file_name, "w") as f:
        f.write(path[1])

    print(f"{path[1]} >> {file_name}")
    path[2] = slot

    conf.save(config)



@command(
    "<slot> <path_id>",
    "Writes path of given <path_id> to specified <slot>. The destination of slot is determined by setting 'slots' + <slot>"
)
def cmd_select(args: Args):
    if len(args.common) < 2:
        print("Not enough arguments. Expected <slot> and <id>")
        return

    config = conf.load()
    slot, path_id = args.common
    select_slot(config, slot, path_id)



@command(
    "<path> [, --slot=<slot_name>]",
    "Saves given path. If the optional argument --slot=<slot_name> is provided, it automatically selects the added path to <slot_name>"
)
def cmd_add(args: Args):
    if len(args.common) < 1:
        print("Missing path argument")
        exit(1)

    config = conf.load()

    for path_id, path, slot in config["paths"]:
        if path == args.common[0]:
            print(f"Path `{path}` is already saved under id `{path_id}`")
            return

    path_id = config["index"]
    config["paths"].append([path_id, args.common[0], "NULL"])
    config["index"] += 1

    if "slot" in args.named:
        select_slot(config, args.named["slot"], path_id)
        return

    conf.save(config)



@command(
    "<id> [, --pattern=<pattern>, --slot=<slot>]",
    "Deletes path with given entry. Use command `ls` to see ids for all saved paths. Use optional arguments to specify path. <pattern> must return specify only one path."
)
def cmd_delete(args: Args):
    config = conf.load()

    index = None
    if "pattern" in args.named:
        temp = utils.indexes_of(config["paths"], lambda p: utils.matches_pattern(args.named["pattern"], p[1]))
        if len(temp) != 1:
            print("Pattern specifies more then one path.")
            exit(1)
        index = temp[0]
    elif "slot" in args.named:
        index = utils.index_of(config["paths"], lambda p: str(p[2]) == args.named["slot"])
    elif len(args.common) == 1:
        index = utils.index_of(config["paths"], lambda p: str(p[0]) == args.common[0])
    else:
        print("Missing path id argument")
        exit(1)

    if index is None:
        print(f"Could not find path")
        return

    slot = config["paths"][index][2]
    if slot != "NULL":
        os.unlink(config["slots"] + slot)

    config["paths"].pop(index)
    conf.save(config)



CYAN = utils.COLOR_CYAN
YELLOW = utils.COLOR_YELLOW
tint = utils.color
@command(
    "[, <pattern>]",
    "Lists all saved paths. Use optional parameter <pattern> to search in saved paths"
)
def cmd_ls(args: Args):
    config = conf.load()
    if len(config["paths"]) == 0:
        print("No paths saved...")
        return

    print(f"[{tint(CYAN, 'ID')}]\t{tint(YELLOW, 'SLOT')}\tPATH")
    argc = len(args.common)
    for path_id, path, slot in config["paths"]:
        if argc > 0 and not utils.matches_pattern(args.common[0], path):
            continue

        print(f"[{tint(CYAN, path_id)}]\t{tint(YELLOW, '' if slot == 'NULL' else slot)}\t{path}")



@command(
    "<name> <value>",
    "Set <value> to <name>. Writeable settings are: 'slots'"
)
def cmd_setting(args: Args):
    if len(args.common) < 2:
        print("Not enough arguments. Expected <setting> and <value>")
        exit(1)

    setting, value = args.common
    if setting in conf.READONLY_SETTINGS:
        print(f"Can not modify read only setting `{setting}`")
        exit(1)

    config = conf.load()
    config[setting] = value
    conf.save(config)

    print(f"{setting}: {value}")

