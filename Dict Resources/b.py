import json

with open("ID Dict - Edited.json", 'r') as file:
    data = json.load(file)

keys = data.keys()
for k in keys:
    if data[k]["minionData"]["multiYield"]:
        for i in range(len(data[k]["items"]["1"])):
            craftN = data[k]["items"]["1"][i].pop("craft")
            prevItem = data[k]["items"]["0"][i]
            data[k]["items"]["1"][i]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}
        if "2" in data[k]["items"]:
            if type(data[k]["items"]["2"]) == list:
                for i in range(len(data[k]["items"]["2"])):
                    craftN = data[k]["items"]["2"][i].pop("craft")
                    prevItem = data[k]["items"]["0"][i]
                    data[k]["items"]["2"][i]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}
            else:
                craftN = data[k]["items"]["2"].pop("craft")
                prevItem = data[k]["items"]["0"][0]
                data[k]["items"]["2"]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}
    else:
        craftN = data[k]["items"]["1"].pop("craft")
        prevItem = data[k]["items"]["0"]
        data[k]["items"]["1"]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}
        if "2" in data[k]["items"]:
            craftN = data[k]["items"]["2"].pop("craft")
            prevItem = data[k]["items"]["0"]
            data[k]["items"]["2"]["craft"] = {"itemUsed": prevItem['gameID'], "number": craftN}

with open("ID Dict - Edited.json", 'w') as file:
    json.dump(data, file)
