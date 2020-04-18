import pandas as pd
import json
import re

minionTiers = pd.read_csv("MinionTiers.csv", header=None)

data = {}
for i in range(0, 665, 13):
    minion = minionTiers.values[i:i+12, :]
    delays = [float(t[:-1]) for t in minion[1:,4]]
    y = re.search(r'(?<=@x)\d+\.{0,1}\d*', minion[0,5])
    data[minion[0,0]] = {
        "minionData": {
            "delays": delays,
            "actionYield": float(y[0]) if y else 1.0,
            "diamondSpreading": True
        }
    }

# Import products list from cached file
with open("prods.json", 'r') as file:
    IDs = json.load(file)["productIds"]

with open("shortcut.json", 'r') as file:
    short = json.load(file)

for k in data.keys():
    data[k]["items"] = {}

    guessID = k.upper()

    if guessID in IDs:
        data[k]["items"][0] = {
            "name": k,
            "gameID": guessID
        }
    elif short[k] in IDs:
        data[k]["items"][0] = {
            "name": k,
            "gameID": short[k]
        }
    else:
        data[k]["items"][0] = {
            "name": k,
            "gameID": "check"
        }

    guessID = "ENCHANTED_" + guessID
    if "ENCHANTED_" + short[k] in IDs:
        data[k]["items"][1] = {
            "name": "Enchanted " + k,
            "gameID": "ENCHANTED_" + short[k],
            "craft": 160
        }
    elif guessID in IDs:
        data[k]["items"][1] = {
            "name": "Enchanted " + k,
            "gameID": guessID,
            "craft": 160
        }
    else:
        data[k]["items"][1] = {
            "name": "Enchanted " + k,
            "gameID": "check",
            "craft": 160
        }

    guessID += "_BLOCK"
    if guessID in IDs:
        data[k]["items"][2] = {
            "name": "Enchanted " + k + " Block",
            "gameID": guessID,
            "craft": 25600
        }
    elif "ENCHANTED_" + short[k] + "_BLOCK" in IDs:
        data[k]["items"][2] = {
            "name": "Enchanted " + k + "_BLOCK",
            "gameID": "ENCHANTED_" + short[k] + "_BLOCK",
            "craft": 25600
        }


with open("ID Dict.json", 'w') as file:
    json.dump(data, file)
