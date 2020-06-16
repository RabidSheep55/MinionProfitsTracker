import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from os.path import join

#### Functions
def parse(x):
    if x < 1000:
        return str(x)
    elif x < 1000000:
        return str(round(x/1000, 1 if x < 100000 else None)) + 'k'
    else:
        return str(round(x/1000000, 1 if x < 100000000 else None)) + 'M'

#### Runtime
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

        # Fish minion only has one type of action, (not break or place)
        if m == "Fish":
            breaksPerH *= 2

        # Compute yields from minons which generate multiple items differently
        # We only consider selling enchanted items at the Bazaar
        if not curr["minionData"]["multiYield"]:
            # Compute Diamond Spreading profits (selling ench diamonds)
            if curr["minionData"]["diamondSpreading"]:
                diaBonus = curr["items"]["0"]["actionYield"] * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160
            else:
                diaBonus = 0

            if "1" in curr["items"]:
                enchPerH = curr["items"]["0"]["actionYield"] * breaksPerH / curr["items"]["1"]["craft"]["number"]
                enchPrice = prices.get(curr["items"]["1"]["gameID"], 0)
                enchProfits[m] = enchPerH * enchPrice + diaBonus

        else:
            # Compute Diamond Spreading profits (selling ench diamonds)
            if curr["minionData"]["diamondSpreading"]:
                avgYield = sum([curr["items"]["0"][i]["actionYield"] for i in range(len(curr["items"]["0"]))])
                diaBonus = 2 * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160
            else:
                diaBonus = 0

            if "1" in curr["items"]:
                enchProfit = 0
                for i in range(len(curr["items"]["1"])):
                    enchPerH = curr["items"]["0"][i]["actionYield"] * breaksPerH / curr["items"]["1"][i]["craft"]["number"]
                    enchPrice = prices.get(curr["items"]["1"][i]["gameID"], 0)
                    enchProfit += enchPerH * enchPrice
                enchProfits[m] = enchProfit + diaBonus

    # Now that all profits have been computed, sort them and find each minon's rank
    profits = [[key, value] for key, value in enchProfits.items()]

    profits.sort(key= lambda a: a[1])
    newKeys = [profit[0] for profit in profits]

    # This ugly bit initializes the dict so that its order is the same order
    # That we will use to plot them (To keep that color cycler uniformity)
    # Should probably find something better as you shouldnt use dict orders
    if lvl == 0:
        ranks = dict(zip(newKeys, [[] for m in mData.keys()]))

    # Save rank values in lists within the minion dict
    # Rank values are saved alongside the actual profit value
    for i in range(len(newKeys)):
        ranks[newKeys[i]] += [(i+1, round(profits[i][1]))]

### Plot results
fig, ax = plt.subplots(constrained_layout=True)

# Set custom rainbow cycler
rainbowCycle = mpl.cycler(color=['C12F1D', 'D94E1F', 'F16C20', 'EF8B2C', 'ECAA38', 'ECAA38', 'EBC844', '89B37D', '1395BA', '117899', '0F5B78', '0D3C55'])
ax.set_prop_cycle(rainbowCycle)

# Create custom rectangle scatter point
h = 1.3
w = 3
vertices = np.array([[-w, -h], [w, -h], [w, h], [-w, h]])
rec = mpl.path.Path(vertices)

# Plot data
lvls = list(range(1, 12))
initOrder = list(ranks.keys())
for m in initOrder:
    rank = [rank[0] for rank in ranks[m]]
    vals = [rank[1] for rank in ranks[m]]
    curr = ax.plot(lvls, rank, lw=3, clip_on=False, zorder=0)
    edgecol = curr[0].get_color()

    # Position and draw profit labels
    for i in range(len(ranks[m])):
        xpos = lvls[i]
        ypos = rank[i]
        ax.add_patch
        ax.text(xpos, ypos, parse(vals[i]),
            fontsize=7,
            zorder=10,
            ha="center",
            va="center",
            bbox=dict(facecolor="#ecf0f1", edgecolor=edgecol, boxstyle='round,pad=0.3', lw=2.2))


# Graph settings
plt.xlim(left=0.7, right=11.5)
plt.ylim(bottom=0.7, top=None)

plt.yticks(list(range(1, len(ranks.keys())+1)), initOrder)
plt.xticks(lvls)
plt.tick_params(axis="both", bottom=False, left=False) #, labelbottom=False, labelleft=False)
plt.xlabel("Minion Level")
plt.title(f"Minion Rank based on profit/hour (top is best) | Lava Bucket \n Bazaar prices updated on {prices['time']} CEST", pad=-30, fontsize=13)

# mplstyle setting ported into code (I use custom .mplsytle files to make this easier usually)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.margins(x=0, y=0)

bg = "#ecf0f1"
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

fig.set_size_inches(7, 13)
fig.savefig(join('Raw Figs','MinionLvlVsRank-EXPERIMENTAL.png'), dpi=300, facecolor=bg, edgecolor=bg)
plt.show()
