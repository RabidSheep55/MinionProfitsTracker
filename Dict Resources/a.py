import json

with open("ID Dict - Edited.json", 'r') as file:
    data = json.load(file)

keys = list(data.keys())
for key in keys:
    if data[key]["minionData"]["multiYield"]:
        actYield = data[key]["minionData"].pop("actionYield")
        data[key]["items"]['0']["actionYield"] = actYield
        o = data[key]["items"]['0']
        data[key]["items"]['0'] = [o, o]
        if "1" in data[key]["items"]:
            i = data[key]["items"]['1']
            data[key]["items"]['1'] = [i, i]

with open("ID Dict - Edited.json", 'w') as file:
    json.dump(data, file)
