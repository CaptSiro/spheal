import json



CONFIG_FILE = "./spheal.json"
READONLY_SETTINGS = ["paths", "index"]



def load():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save(conf):
    with open(CONFIG_FILE, "w") as f:
        json.dump(conf, f)
