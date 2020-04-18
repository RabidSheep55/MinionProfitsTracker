import json

with open("ID Dict - Edited.json", 'r') as file:
    data = json.load(file)

keys = list(data.keys())
links = {}

for k in keys:
    if not data[k]["minionData"]["multiYield"]:
        links[data[k]["items"]["0"]["name"]] = data[k]["items"]["0"]["gameID"]
    else:
        for item in data[k]["items"]["0"]:
            links[item["name"]] = item["gameID"]

with open("f.json", 'w') as file:
    json.dump(links, file)
