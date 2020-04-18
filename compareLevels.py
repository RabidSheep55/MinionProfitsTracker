import json
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('rank_viewer')

# Import Minion/ID data
with open("ID Dict - Edited.json", 'r') as file:
    mData = json.load(file)

# Import prices
with open("prices.json", 'r') as file:
    prices = json.load(file)

# Define setup
fuel = 1.25

#### Find each minion rank based on level
minions = list(mData.keys())

for lvl in range(0, 11, 1):
    enchProfits = {}
    for m in minions:
        curr = mData[m]
        breaksPerH = (3600 / curr["minionData"]["delays"][lvl]) * fuel * 0.5

        if curr["minionData"]["diamondSpreading"]:
            diaBonus = 2 * breaksPerH * 0.1 * prices["ENCHANTED_DIAMOND"] / 160

        if m == "Fish":
            breaksPerH *= 2

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

    keys = list(enchProfits.keys())
    profits = []
    for k in keys:
        profits += [(k, enchProfits.get(k, 0))]

    profits.sort(key= lambda a: a[1])
    newKeys = [profit[0] for profit in profits]

    if lvl == 0:
        ranks = dict(zip(newKeys, [[] for m in minions]))

    for i in range(len(newKeys)):
        ranks[newKeys[i]] += [i+1]

### Plot results
fig, ax = plt.subplots()

lvls = list(range(1, 12))
initOrder = list(ranks.keys())
for m in initOrder:
    ax.plot(lvls, ranks[m], lw=2)
    ax.scatter(lvls, ranks[m])

plt.yticks(list(range(1, len(ranks.keys())+1)), initOrder)
plt.xticks(lvls)
plt.ylim(bottom=0)
plt.xlim(left=0.9, right=11.5)
plt.tick_params(axis="both", bottom=False, left=False)
plt.xlabel("Minion Level")
plt.title(f"Minion Rank based on profit/hour (top is best) | Lava Bucket \n Bazaar prices updated on {prices['time']} CEST")

bg = "#ecf0f1"

fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

plt.tight_layout()
fig.set_size_inches(8, 12)
fig.savefig('Raw Figs\MinionLvlVsRank.png', dpi=300, facecolor=bg, edgecolor=bg)
plt.show()
