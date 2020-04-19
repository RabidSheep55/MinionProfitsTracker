import json
import matplotlib.pyplot as plt
import numpy as np

# Import Minion/ID data
with open(r"Resources\minionDataDict.json", 'r') as file:
    mData = json.load(file)

# Import bazaar prices
with open(r"Resources\bazaarPrices.json", 'r') as file:
    prices = json.load(file)

### MINION LEVEL SELECTION
# Set your desired minion level starting from 0
# So a level 5 minion has lvl=4
# (Note: you can set max level by setting lvl=-1)
lvl = -1 # Max level

#### Compute yields from each minion
enchProfits = {}
# Iterate through every minion
for m in mData.keys():
    curr = mData[m]
    breaksPerH = (3600 / curr["minionData"]["delays"][lvl]) * 0.5

    # Compute Diamond Spreading profits (selling ench diamonds)
    if curr["minionData"]["diamondSpreading"]:
        diaBonus = 2 * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160

    # Fish minion only has one type of action, (not break or place)
    if m == "Fish":
        breaksPerH *= 2

    # Compute yields from minons which generate multiple items differently
    # Only concerned with the enchanted type sold here
    if not curr["minionData"]["multiYield"]:
        if "1" in curr["items"]:
            enchPerH = curr["items"]["0"]["actionYield"] * breaksPerH / curr["items"]["1"]["craft"]["number"]
            enchPrice = prices.get(curr["items"]["1"]["gameID"], 0)
            enchProfits[m] = enchPerH * enchPrice + diaBonus

    else:
        if "1" in curr["items"]:
            enchProfit = 0
            for i in range(len(curr["items"]["1"])):
                enchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["1"][i]["craft"]["number"]
                enchPrice = prices.get(curr["items"]["1"][i]["gameID"], 0)
                enchProfit += enchPerH * enchPrice
            enchProfits[m] = enchProfit + diaBonus

#### Sort minons by profit
# keys = list(enchProfits.keys())
profits = [[key, value] for key, value in enchProfits.items()]
# for k in keys:
#     profits += [(k, enchProfits.get(k, 0))]

profits.sort(key= lambda a: a[1], reverse=True)
newKeys = [profit[0] for profit in profits]
ench = np.array([profit[1] for profit in profits])

#### Compute effect of Fuel Bonuses
wheelPricePerH = prices.get("HAMSTER_WHEEL", 0)/24
wheelBonus = 0.5
wheelProfit = ench*(wheelBonus+1) - wheelPricePerH

catalystPricePerH = prices.get("CATALYST", 0)/5
catalystBonus = 3
catalystProfit = ench*catalystBonus - catalystPricePerH

fleshPricePerH = prices.get("FOUL_FLESH", 0)/3
fleshBonus = 0.9
fleshProfit = ench*(fleshBonus+1) - fleshPricePerH

lavaBonus = 0.25
lavaProfit = ench*(lavaBonus+1)

##### Plot Results
fig, ax = plt.subplots()

[c1, c2, c3, c4, c5] = ["#f1c40f", "#e67e22", "#e74c3c", "#1abc9c", "#3498db"]
for i in range(len(newKeys)):
    s = [(c1, ench[i]),
         (c2, wheelProfit[i]),
         (c3, catalystProfit[i]),
         (c4, fleshProfit[i]),
         (c5, lavaProfit[i])]
    s.sort(key= lambda a: abs(a[1]), reverse=True)
    for p in s:
        ax.bar(newKeys[i], p[1], color=p[0], alpha=1 if p[1]>0 else 0.2)

# Add legend entries
ax.bar(newKeys[1], 0, color=c1, label="None")
ax.bar(newKeys[1], 0, color=c2, label="Hamster Wheel")
ax.bar(newKeys[1], 0, color=c3, label="Catalyst")
ax.bar(newKeys[1], 0, color=c4, label="Foul Flesh")
ax.bar(newKeys[1], 0, color=c5, label="Lava Bucket")

### Figure Settings
ax.set_ylabel("Profit/h")
plt.legend(title="Fuels")
plt.title(f"Profit / hour / minion | Ench items sold | Minion lvl {lvl+1 if lvl>0 else 11} \n Bazaar prices updated on {prices['time']} CEST", pad=-10, fontsize=13)

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
fig.savefig(f'Raw Figs\FuelsLvl{lvl+1 if lvl>0 else "Max"}.png', dpi=300, facecolor=bg, edgecolor=bg)
plt.show()
