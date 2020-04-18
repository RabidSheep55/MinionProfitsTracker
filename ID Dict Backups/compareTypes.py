import json
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('clean_gridless')

# Import Minion/ID data
with open("ID Dict - Edited.json", 'r') as file:
    mData = json.load(file)

# Import prices
with open("prices.json", 'r') as file:
    prices = json.load(file)

# Define setup
lvl = 4 # Max level
fuel = 1.25

# Find each minion yield
minions = list(mData.keys())
baseProfits = {}
enchProfits = {}
superEnchProfits = {}
for m in minions:
    curr = mData[m]
    breaksPerH = (3600 / curr["minionData"]["delays"][lvl]) * fuel * 0.5

    if m == 'Fish':
        breaksPerH *= 2

    if curr["minionData"]["diamondSpreading"]:
        diaBonus = 2 * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160

    if not mData[m]["minionData"]["multiYield"]:
        basePerH = curr["items"]["0"]["actionYield"] * breaksPerH
        basePrice = prices.get(curr["items"]["0"]["gameID"], 0)
        baseProfits[m] = basePerH * basePrice + diaBonus

        if "1" in curr["items"]:
            enchPerH = basePerH / curr["items"]["1"]["craft"]["number"]
            enchPrice = prices.get(curr["items"]["1"]["gameID"], 0)
            enchProfits[m] = enchPerH * enchPrice + diaBonus

        if "2" in curr["items"]:
            superEnchPerH = basePerH / curr["items"]["2"]["craft"]["number"]
            superEnchPrice = prices.get(curr["items"]["2"]["gameID"], 0)
            superEnchProfits[m] = superEnchPerH * superEnchPrice + diaBonus

    else:
        baseProfit = 0
        for i in range(len(curr["items"]["0"])):
            basePerH = curr["items"]["0"][i]["actionYield"] * breaksPerH
            basePrice = prices.get(curr["items"]["0"][i]["gameID"], 0)
            baseProfit += basePerH * basePrice
        baseProfits[m] = baseProfit + diaBonus

        if "1" in curr["items"]:
            enchProfit = 0
            for i in range(len(curr["items"]["1"])):
                enchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["1"][i]["craft"]["number"]
                enchPrice = prices.get(curr["items"]["1"][i]["gameID"], 0)
                enchProfit += enchPerH * enchPrice
            enchProfits[m] = enchProfit + diaBonus

        if "2" in curr["items"]:
            superEnchProfit = 0
            for i in range(len(curr["items"]["2"])):
                superEnchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["2"][i]["craft"]["number"]
                superEnchPrice = prices.get(curr["items"]["2"][i]["gameID"], 0)
                superEnchProfit += superEnchPerH * superEnchPrice
            superEnchProfits[m] = superEnchProfit + diaBonus


# plt.bar([k for k in baseProfits], [v for v in baseProfits.values()], color="yellow", alpha=0.2, label="Base")
# plt.bar([k for k in enchProfits], [v for v in enchProfits.values()], color="teal", alpha=0.5, label="Enchanted")
# plt.bar([k for k in superEnchProfits], [v for v in superEnchProfits.values()], color="magenta", alpha=0.5, label="Super Enchanted")
#
# plt.ylabel("Profit/h (max lvl + lava)")
# plt.legend()

# plt.xticks(rotation=90)
# plt.show()

keys = list(baseProfits.keys())
profits = []
for k in keys:
    profits += [(k, baseProfits.get(k, 0), enchProfits.get(k, 0), superEnchProfits.get(k, 0))]

profits.sort(key= lambda a: a[2], reverse=True)
newKeys = [profit[0] for profit in profits]
base = [profit[1] for profit in profits]
ench = [profit[2] for profit in profits]
superEnch = [profit[3] for profit in profits]

plt.bar(newKeys, base, color="yellow", alpha=0.2, label="Base")
plt.bar(newKeys, ench, color="teal", alpha=0.5, label="Enchanted")
plt.bar(newKeys, superEnch, color="magenta", alpha=0.5, label="Super Enchanted")

plt.ylabel("Profit/h (max lvl + lava)")
plt.legend(title="Type Sold at Bazaar")

plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
