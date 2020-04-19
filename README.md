# The FREE Minion Profits Tracker Scripts
Tired of guessing which minion is the most profitable? Tired of going through each minion using a huge brain script 'made available' by an influencer? Tired of spending hours changing minion levels on a spreadsheet? Tired of being poor, uncertain and in the dark about bazaar fluctuations? Well I present to you, **the FREE minion profits calculator script!**

## Features
 - Update bazaar prices automatically
 - Minion speeds, drops and merchant sell prices already stored
 - Compare item types sold to bazaar (base, enchanted or super-enchanted)
 - Easily compare fuel viabilities
 - Display data for every minion at once on really spicy looking graphs:

## Example Graphs
### Fuels [adding more soon]
This takes into account the price of the fuel per hour, as you can see, some fuel choices result in a net loss.
FuelsLvlMax.png

### Types sold
Some items might be worth selling to the merchant, or as their super-enchanted form to maximise profit. (I left the base price here, but it's a bit unfeasible as minions would fill up insanely quickly)
TypesLvlMax.png

### Minion rank
This one shows the evolution of the minion's rank in terms of profit, as it is leveled up.
MinionLvlVsRank.png

## How to Use
### Dependencies
In order to run this you'll need to have Python installed with the following modules:
```
matplotlib, json, requests, re, numpy, datetime
```
*(I won't be explaining how to download and setup python here, there are plenty of resources online for that! If you're running windows, I can still recommend the Anaconda environment as it already has most of the packages you need)*

### Install
To get the scripts for yourself, simply clone or download this repo on your computer. Make sure you store the Resources folder in the same directory in which you are running the scripts!

### API Key
In order to automatically fetch the bazaar prices you'll need to provide your own Hypixel API key. To do this, simply hop into a lobby, and in-game type the following command:
```
/api
```
Copy the output key, and save it in a file called `creds.txt` in the **Resources** folder (the fetchPrices.py script will need that file to authenticate your requests to the API).

## Running the Scipts
Great! Now that you have al the prerequisites setup, all you need to do is fetch the bazaar prices by running the `fetchPrices.py` script first (this will take a while, as each item is fetched independantly), and run whichever comparison tool you want!

## Acknowledgements
Thanks to TBlazeWarriorT, I used a lot of the minion data from his famous spreadsheet, on top of painfully collecting my own.
Thanks to ThirtyVirus for providing the adequate situation in which I could release this tool.
If you spot any inconsistencies in the graphs or in the code, please let me know!!
