import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from os.path import join

# Import Minion/ID data
with open(join("Resources","minionDataDict.json"), 'r') as file:
    mData = json.load(file)

# Import bazaar prices
with open(join("Resources","bazaarPrices.json"), 'r') as file:
    prices = json.load(file)

### Fuel Multiplier Setup
fuel = 1.25 # Ench Lava Bucket

#### Find each minion's profit rank based on level
# Iterate for each minion level
for lvl in range(0, 11, 1):
    enchProfits = {}
    # Iterate for each minion
    for m in mData.keys():
        curr = mData[m] # Current minion
        breaksPerH = (3600 / curr["minionData"]["delays"][lvl]) * fuel * 0.5

        # Compute Diamond Spreading profits (selling ench diamonds to Bazaar)
        if curr["minionData"]["diamondSpreading"]:
            diaBonus = 2 * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160
        else:
            diaBonus = 0

        # Fish minion only has one type of action, (not break or place)
        if m == "Fish":
            breaksPerH *= 2

        # Compute yields from minons which generate multiple items differently
        # We only consider selling enchanted items at the Bazaar
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

    # Now that all profits have been computed, sort them and find each minon's rank
    # keys = list(enchProfits.keys())
    profits = [[key, value] for key, value in enchProfits.items()]
    # for k in keys:
    #     profits += [(k, enchProfits.get(k, 0))]

    profits.sort(key= lambda a: a[1])
    newKeys = [profit[0] for profit in profits]

    # This ugly bit initializes the dict so that its order is the same order
    # That we will use to plot them (To keep that color cycler uniformity)
    # Should probably find something better as you shouldnt use dict orders
    if lvl == 0:
        ranks = dict(zip(newKeys, [[] for m in mData.keys()]))

    # Save rank values in lists within the minion dict
    for i in range(len(newKeys)):
        ranks[newKeys[i]] += [i+1]

### Plot results
fig, ax = plt.subplots()

# Set custom rainbow cycler
rainbowCycle = mpl.cycler(color=['C12F1D', 'D94E1F', 'F16C20', 'EF8B2C', 'ECAA38', 'ECAA38', 'EBC844', '89B37D', '1395BA', '117899', '0F5B78', '0D3C55'])
ax.set_prop_cycle(rainbowCycle)

lvls = list(range(1, 12))
initOrder = list(ranks.keys())
for m in initOrder:
    ax.plot(lvls, ranks[m], lw=2)
    ax.scatter(lvls, ranks[m])

# Graph settings
plt.yticks(list(range(1, len(ranks.keys())+1)), initOrder)
plt.xticks(lvls)
plt.ylim(bottom=0)
plt.xlim(left=0.9, right=11.5)
plt.tick_params(axis="both", bottom=False, left=False)
plt.xlabel("Minion Level")
plt.title(f"Minion Rank based on profit/hour (top is best) | Lava Bucket \n Bazaar prices updated on {prices['time']} CEST", pad=-10, fontsize=13)

# mplstyle setting ported into code (I use custom .mplsytle files to make this easier usually)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.margins(x=0, y=0)

bg = "#ecf0f1"
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

plt.tight_layout()
fig.set_size_inches(8, 12)
fig.savefig('Raw Figs\MinionLvlVsRank.png', dpi=300, facecolor=bg, edgecolor=bg)
plt.show()
