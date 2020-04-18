import requests as rq
import json
from time import sleep
from datetime import datetime

#### Constants
# URL to fetch bazaar data from
BASE_URL = r"https://api.hypixel.net/skyblock/bazaar/product"

# Fetch API key from creds.txt
with open("creds", 'r') as file:
    KEY = str(file.readlines()[0].rstrip())

#### Functions
# Print json objects (for debugging)
def jpr(o):
    print(json.dumps(o, indent=3))

# Fetch item IDs from API (don't need to do this every time)
def importIDs():
    # Setup parameter packet for get request
    p = {"key": KEY}

    # Send request
    response = rq.get(BASE_URL + "s", params=p)
    print(f"Item ID fetcher code: {response.status_code}")

    # Extract and save products response into file
    with open("itemIDs.json", 'w') as file:
        json.dump(response.json(), file)
    print("Successfully saved item IDs")

# Import item IDs from cached file
def importIDsFile():
    # Import products list from cached file
    with open("itemIDs.json", 'r') as file:
        raw = json.load(file)
    return raw["productIds"]

# Fetch product price from ID
def getPrice(id):
    # Setup parameter packet for get request
    p = {"key": KEY, "productId": id}

    # Send get request
    response = rq.get(BASE_URL, params=p)

    if response.status_code == 200:
        # Extract price from quick status response
        price = float(response.json()["product_info"]["quick_status"]["buyPrice"])
        return price
    else:
        print(f"[GETPRICE] {item} ERROR:{response.status_code}")
        return None

# Update ID list?
# importIDs()

### Runtime
# Get all time ID list
itemIDs = importIDsFile()

# Set date for recording purposes
prices = {}
prices["time"] = datetime.now().strftime(r"%A %d %b - %H:%M %Z")
print(f"[TIME] {prices['time']}")

# Get the price of each item
i = 0
for item in itemIDs:
    i += 1
    prices[item] = getPrice(item)
    print(f"[getPrice {i}/{len(itemIDs)}] {item} price : {prices[item]}")
    sleep(0.7)

with open("prices.json", 'w') as file:
    json.dump(prices, file)
