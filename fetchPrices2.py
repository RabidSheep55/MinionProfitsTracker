import requests as rq
import json
from datetime import datetime
from os.path import join

# URL to fetch bazaar data from (sky.lea.moe)
BASE_URL = r"https://sky.lea.moe/api/bazaar"

# Get prices from API
response = rq.get(BASE_URL)
if response.status_code == 200:
    pricesList = response.json()
else:
    print(f"Error getting Bazaar Prices | Code: {response.status_code}")

# Format list into dict with ID keys
pricesDict = {}
for item in pricesList:
    pricesDict[item["id"]] = item["price"]

# Set date for recording purposes
pricesDict["time"] = datetime.now().strftime(r"%A %d %b - %H:%M")

# Save item prices in json file
with open(join("Resources","bazaarPrices.json"), 'w') as file:
    json.dump(pricesDict, file, indent=3)
