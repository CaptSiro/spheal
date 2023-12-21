import json
import sys
import os


os.chdir(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FILE = "./spheal.json"
READONLY_SETTINGS = ["paths", "index"]


def conf_load():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def conf_save(conf):
    with open(CONFIG_FILE, "w") as f:
        json.dump(conf, f)


def todo(message: str):
    print(f"Todo: {message}")
    exit(1)


def cmd_help(program: str):
    print(f"Usage: {program} <command>")
    print(f"\n\t[, help]\n\t\tShows this help")
    print(f"\n\tadd path [, --slot=<slot_name>]\n\t\tAdds path but it is not selected")
    print(f"\n\tdelete id\n\t\tDeletes path with given entry. Use command `ls` to see ids for all saved paths")
    print(f"\n\tls [, pattern]\n\t\tLists all saved paths. Use optional parameter pattern to search in saved paths")
    print(f"\n\tset setting value\n\t\tSets value of specified setting\n\t\t\tWriteable settings: slots")
    print(f"\n\tselect slot id\n\t\tWrites path of given id to specified slot. Slot is number and it is appended to the path of setting 'slots'")


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



def cmd_add(args: Args):
    if len(args.common) < 1:
        print("Missing path argument")
        exit(1)

    conf = conf_load()

    for path_id, path, slot in conf["paths"]:
        if path == args.common[0]:
            print(f"Path `{path}` is already saved under id `{path_id}`")
            return

    path_id = conf["index"]
    conf["paths"].append([path_id, args.common[0], "NULL"])
    conf["index"] += 1

    if "slot" in args.named:
        select_slot(conf, args.named["slot"], path_id)
        return

    conf_save(conf)


def index_of(array, predicate):
    for i, v in enumerate(array):
        if predicate(v):
            return i

    return None
def cmd_delete(args: Args):
    if len(args.common) < 1:
        print("Missing path id argument")
        exit(1)

    conf = conf_load()

    index = index_of(conf["paths"], lambda p: str(p[0]) == str(args.common[0]))
    if index is None:
        print(f"Could not find path with id `{args.common[0]}`")
        return

    slot = conf["paths"][index][2]
    if slot != "NULL":
        os.unlink(conf["slots"] + slot)

    conf["paths"].pop(index)
    conf_save(conf)


COLOR_CYAN = "\u001b[36m"
COLOR_YELLOW = "\u001b[33;1m"
COLOR_RESET = "\u001b[0m"
def color(c: str, text) -> str:
    return c + str(text) + COLOR_RESET
def matches_pattern(pattern, subject):
    pattern_length = len(pattern)
    pattern_index = 0

    for i in range(len(subject)):
        if pattern[pattern_index] == subject[i]:
            pattern_index += 1

            if pattern_length == pattern_index:
                return True

    return False
def cmd_ls(args: Args):
    conf = conf_load()
    if len(conf["paths"]) == 0:
        print("No paths saved...")
        return

    print(f"[{color(COLOR_CYAN, 'ID')}]\t{color(COLOR_YELLOW, 'SLOT')}\tPATH")
    argc = len(args.common)
    for path_id, path, slot in conf["paths"]:
        if argc > 0 and not matches_pattern(args.common[0], path):
            continue

        print(f"[{color(COLOR_CYAN, path_id)}]\t{color(COLOR_YELLOW, '' if slot == 'NULL' else slot)}\t{path}")


def cmd_set(args: Args):
    if len(args.common) < 2:
        print("Not enough arguments. Expected <setting> and <value>")
        exit(1)

    setting, value = args.common
    if setting in READONLY_SETTINGS:
        print(f"Can not modify read only setting `{setting}`")
        exit(1)

    conf = conf_load()
    conf[setting] = value
    conf_save(conf)

    print(f"{setting}: {value}")


def select_slot(conf, slot, path_id):
    i = index_of(conf["paths"], lambda p: str(p[0]) == str(path_id))
    if i is None:
        print(f"Could not find path with id `{path_id}`")
        return

    path = conf["paths"][i]

    old = index_of(conf["paths"], lambda p: str(p[2]) == str(slot))
    if old is not None:
        os.unlink(conf["slots"] + conf["paths"][old][2])
        conf["paths"][old][2] = "NULL"

    file_name = conf["slots"] + str(slot)
    with open(file_name, "w") as f:
        f.write(path[1])

    print(f"{path[1]} >> {file_name}")
    path[2] = slot

    conf_save(conf)
def cmd_select(args: Args):
    if len(args.common) < 2:
        print("Not enough arguments. Expected <slot> and <id>")
        return

    conf = conf_load()
    slot, path_id = args.common
    select_slot(conf, slot, path_id)


def main():
    program = sys.argv[0] or "<program>"

    if len(sys.argv) < 2:
        cmd_help(program)
        return

    _, command, *arg_list = sys.argv
    args = Args.parse(arg_list)

    if command == "help":
        cmd_help(program)
    elif command == "add":
        cmd_add(args)
    elif command == "delete":
        cmd_delete(args)
    elif command == "ls":
        cmd_ls(args)
    elif command == "set":
        cmd_set(args)
    elif command == "select":
        cmd_select(args)
    else:
        print(f"Unknown command: <{command}>")
        cmd_help(program)


if __name__ == "__main__":
    main()