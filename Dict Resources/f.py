import json

with open("f.json", 'r') as file:
    prices = json.load(file)

for k in prices.keys():
    if prices[k]["merchPrice"] == 0.0:
        print(f"key:{k} - name:{prices[k]['name']} - price:", end="")
        prices[k]["merchPrice"] = float(input())
        with open("g.json", 'w') as file:
            json.dump(prices, file)
