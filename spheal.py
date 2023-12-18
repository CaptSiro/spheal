import json
import sys



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
    print(f"\t{program} [, help]\n\t\tShows this help")
    print(f"\t{program} add path\n\t\tAdds path but it is not selected")
    print(f"\t{program} delete id\n\t\tDeletes path with given entry. Use command `ls` to see ids for all saved paths")
    print(f"\t{program} ls [, pattern]\n\t\tLists all saved paths in `[id] path` format. Use optional parameter pattern to search in saved paths")
    print(f"\t{program} set setting value\n\t\tSets value of specified setting\n\t\t\tWriteable settings: slots")
    print(f"\t{program} select slot id\n\t\tWrites path of given id to specified slot. Slot is number and it is appended to the path of setting 'slots'")


def cmd_add(args):
    if len(args) < 1:
        print("Missing path argument")
        exit(1)

    conf = conf_load()

    for path_id, path in conf["paths"]:
        if path == args[0]:
            print(f"Path `{path}` is already saved under id `{path_id}`")
            return

    conf["paths"].append([conf["index"], args[0]])
    conf["index"] += 1
    conf_save(conf)


def index_of(array, predicate):
    for i, v in enumerate(array):
        if predicate(v):
            return i

    return None
def cmd_delete(args):
    if len(args) < 1:
        print("Missing path id argument")
        exit(1)

    conf = conf_load()

    index = index_of(conf["paths"], lambda p: str(p[0]) == str(args[0]))
    if index is None:
        print(f"Could not find path with id `{args[0]}`")
        return

    conf["paths"].pop(index)
    conf_save(conf)


def matches_pattern(pattern, subject):
    pattern_length = len(pattern)
    pattern_index = 0

    for i in range(len(subject)):
        if pattern[pattern_index] == subject[i]:
            pattern_index += 1

            if pattern_length == pattern_index:
                return True

    return False
def cmd_ls(args):
    conf = conf_load()
    if len(conf["paths"]) == 0:
        print("No paths saved...")
        return

    argc = len(args)
    for path_id, path in conf["paths"]:
        if argc > 0 and not matches_pattern(args[0], path):
            continue

        print(f"[{path_id}] {path}")


def cmd_set(args):
    if len(args) < 2:
        print("Not enough arguments. Expected <setting> and <value>")
        exit(1)

    setting, value = args
    if setting in READONLY_SETTINGS:
        print(f"Can not modify read only setting `{setting}`")
        exit(1)

    conf = conf_load()
    conf[setting] = value
    conf_save(conf)

    print(f"{setting}: {value}")


def cmd_select(args):
    if len(args) < 2:
        print("Not enough arguments. Expected <slot> and <id>")
        return

    conf = conf_load()
    slot, path_id = args
    i = index_of(conf["paths"], lambda p: str(p[0]) == str(path_id))
    if i is None:
        print(f"Could not find path with id `{path_id}`")
        return

    path = conf["paths"][i]
    file_name = conf["slots"] + str(slot)
    with open(file_name, "w") as f:
        f.write(path[1])

    print(f"{path[1]} >> {file_name}")


def main():
    program = sys.argv[0] or "<program>"

    if len(sys.argv) < 2:
        cmd_help(program)
        return


    _, command, *args = sys.argv
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