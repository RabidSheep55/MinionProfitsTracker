import json

with open("ID Dict - Edited.json", 'r') as file:
    data = json.load(file)

keys = data.keys()
for k in keys:
    if not data[k]["minionData"]["multiYield"]:
        craftN = data[k]["items"]["1"].pop("craft")
        prevItem = data[k]["items"]["0"]
        data[k]["items"]["1"]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}
        if "2" in data[k]["items"]:
            craftN = data[k]["items"]["2"].pop("craft")
            prevItem = data[k]["items"]["0"]
            data[k]["items"]["2"]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}

# with open("f.json", 'w') as file:
#     json.dump(data, file)

with open("ID Dict - Edited.json", 'w') as file:
    json.dump(data, file)
