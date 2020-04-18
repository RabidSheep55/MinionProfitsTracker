import pandas as pd
import json
import re

prices = pd.read_csv("MerchantPrices.csv", header=None)

with open("items.json", 'r') as file:
    items = json.load(file)

names = prices.values[:, 0]
merch = prices.values[:, 1]
prices = dict(zip(names, merch))

vals = {}
for k in items.keys():
    if k in prices:
        vals[items[k]] = {
            "name": k,
            "merchPrice": prices[k]
        }
    else:
        vals[items[k]] = {
            "name": "CHECK",
            "merchPrice": "CHECK"
        }

with open("f.json", 'w') as file:
    json.dump(vals, file)
