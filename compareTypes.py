import json
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
import sys

# Import Minion/ID data
with open(join("Resources","minionDataDict.json"), 'r') as file:
    mData = json.load(file)

# Import bazaar prices
with open(join("Resources","bazaarPrices.json"), 'r') as file:
    prices = json.load(file)

# Import merchant prices
with open(join("Resources","merchantSellValues.json"), 'r') as file:
    merchSellValues = json.load(file)

### MINION LEVEL SELECTION
# Set your desired minion level starting from 0 (can now do that via cmd-line arg)
# So a level 5 minion has lvl=4
# (Note: you can set max level by setting lvl=-1)
lvl = -1 if len(sys.argv) == 1 else int(sys.argv[1]) - 1  # Max level
print(f"Minion lvl {lvl+1 if lvl>0 else 11}")

### Fuel Multiplier Setup
fuel = 1.25 # Ench Lava Bucket

#### Compute yields from each minion
baseProfits = {}
enchProfits = {}
superEnchProfits = {}
merchProfits = {}
for m in mData.keys():
    curr = mData[m] # Current minion
    breaksPerH = (3600 / curr["minionData"]["delays"][lvl]) * fuel * 0.5

    # Fish minion only has one type of action, (not break or place)
    if m == 'Fish':
        breaksPerH *= 2

    # Compute yields from minons which generate multiple items differently
    if not mData[m]["minionData"]["multiYield"]:
        # Compute Diamond Spreading profits
        if curr["minionData"]["diamondSpreading"]:
            diaBonus = curr["items"]["0"]["actionYield"] * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160
            merchDiaBonus = curr["items"]["0"]["actionYield"] * breaksPerH * 0.1 * merchSellValues["DIAMOND"]["merchSellValue"]
        else:
            diaBonus = 0

        basePerH = curr["items"]["0"]["actionYield"] * breaksPerH
        basePrice = prices.get(curr["items"]["0"]["gameID"], 0)
        baseProfits[m] = basePerH * basePrice + diaBonus

        # Compute Merchant Profits
        if curr["items"]["0"]["gameID"]:
            merchPrice = merchSellValues[curr["items"]["0"]["gameID"]]["merchSellValue"]
        else:
            merchPrice = 0
            print(f"[ERROR] Price for {m} Minion Not found")
        merchProfits[m] = basePerH * merchPrice + merchDiaBonus

        # Enchanted Item Profits
        if "1" in curr["items"]:
            enchPerH = basePerH / curr["items"]["1"]["craft"]["number"]
            enchPrice = prices.get(curr["items"]["1"]["gameID"], 0)
            enchProfits[m] = enchPerH * enchPrice + diaBonus

        # Super Enchanted Item Profits
        if "2" in curr["items"]:
            superEnchPerH = basePerH / curr["items"]["2"]["craft"]["number"]
            superEnchPrice = prices.get(curr["items"]["2"]["gameID"], 0)
            superEnchProfits[m] = superEnchPerH * superEnchPrice + diaBonus

    else:
        # Compute Diamond Spreading profits
        if curr["minionData"]["diamondSpreading"]:
            avgYield = np.average([curr["items"]["0"][i]["actionYield"] for i in range(len(curr["items"]["0"]))])
            diaBonus = avgYield * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160
            merchDiaBonus = avgYield * breaksPerH * 0.1 * merchSellValues["DIAMOND"]["merchSellValue"]
        else:
            diaBonus = 0

        baseProfit = 0
        merchProfit = 0
        for i in range(len(curr["items"]["0"])):
            basePerH = curr["items"]["0"][i]["actionYield"] * breaksPerH
            basePrice = prices.get(curr["items"]["0"][i]["gameID"], 0)
            baseProfit += basePerH * basePrice

            if curr["items"]["0"][i]["gameID"]:
                merchPrice = merchSellValues[curr["items"]["0"][i]["gameID"]]["merchSellValue"]
            else:
                merchPrice = 0
                print(f"[ERROR] {m} Minion")
            merchProfit += merchPrice * basePerH

        baseProfits[m] = baseProfit + diaBonus
        merchProfits[m] = merchProfit + merchDiaBonus

        # Enchanted Item Profits
        if "1" in curr["items"]:
            enchProfit = 0
            for i in range(len(curr["items"]["1"])):
                enchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["1"][i]["craft"]["number"]
                enchPrice = prices.get(curr["items"]["1"][i]["gameID"], 0)
                enchProfit += enchPerH * enchPrice
            enchProfits[m] = enchProfit + diaBonus

        # Super Enchanted Item Profits
        if "2" in curr["items"]:
            superEnchProfit = 0
            for i in range(len(curr["items"]["2"])):
                superEnchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["2"][i]["craft"]["number"]
                superEnchPrice = prices.get(curr["items"]["2"][i]["gameID"], 0)
                superEnchProfit += superEnchPerH * superEnchPrice
            superEnchProfits[m] = superEnchProfit + diaBonus

### Sort minions by Enchanted item profits
sorter = [[key, value] for key, value in enchProfits.items()]
sorter.sort(key= lambda a: a[1], reverse=True)
newKeys = [key[0] for key in sorter] # Sorted list of keys

### Plot results (making sure to not overlap bars)
fig, ax = plt.subplots()
[c1, c2, c3, c4] = ["#f1c40f", "#e67e22", "#e74c3c", "#1abc9c"]
for k in newKeys:
    s = [(c1, baseProfits.get(k, 0)),
         (c2, enchProfits.get(k, 0)),
         (c3, superEnchProfits.get(k, 0)),
         (c4, merchProfits.get(k, 0))]
    s.sort(key= lambda a: abs(a[1]), reverse=True)
    for p in s:
        ax.bar(k, p[1], color=p[0], alpha=1)

# Add legend entries
ax.bar(newKeys[1], 0, color=c1, label="Base Bazaar")
ax.bar(newKeys[1], 0, color=c2, label="Enchanted Bazaar")
ax.bar(newKeys[1], 0, color=c3, label="Super Enchanted Bazaar")
ax.bar(newKeys[1], 0, color=c4, label="Base Merchant")

### Figure Settings
ax.set_ylabel("Profit/h")
plt.legend(title="Types and Place Sold")
plt.title(f"Profit / hour / minion | Lava Bucket | Minion lvl {lvl+1 if lvl>0 else 11} \n Bazaar prices updated on {prices['time']} CEST", pad=-10, fontsize=13)

# mplstyle setting ported into code (I use custom .mplsytle files to make this easier usually)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.minorticks_on()
ax.xaxis.set_tick_params(which='minor', bottom=False)
ax.margins(x=0, y=0)

ax.spines['bottom'].set_position('zero')
plt.xticks(rotation=90)
plt.tight_layout()

bg = "#ecf0f1"
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

fig.set_size_inches(20, 5)
fig.savefig(f'Raw Figs\TypesLvl{lvl+1 if lvl>0 else "Max"}.png', dpi=300, facecolor=bg, edgecolor=bg)
plt.show()
