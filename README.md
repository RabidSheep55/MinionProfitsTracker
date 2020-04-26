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
![Fuel Profits Comparison Graph](https://github.com/RabidSheep55/MinionProfitsTracker/blob/master/Images/FuelsLvlMax%20-%20Example.png)

### Types sold
Some items might be worth selling to the merchant, or as their super-enchanted form to maximise profit. (I left the base price here, but it's a bit unfeasible as minions would fill up insanely quickly)
![Item type and place Profits comparison graph](https://github.com/RabidSheep55/MinionProfitsTracker/blob/master/Images/TypesLvlMax%20-%20Example.png)

### Minion rank
This one shows the evolution of the minion's rank in terms of profit, as it is leveled up.
![Minion Level Profit Rank Visualizer](https://github.com/RabidSheep55/MinionProfitsTracker/blob/master/Images/MinionLvlVsRank%20-%20Example.png)

## How to Use
### Dependencies
In order to run this you'll need to have Python installed with the following modules:
```
matplotlib, json, requests, re, numpy, datetime
```
*(I won't be explaining how to download and setup python here, there are plenty of resources online for that! If you're running windows, I can still recommend the Anaconda environment as it already has most of the packages you need)*

### Install
To get the scripts for yourself, simply clone or download this repo on your computer. Make sure you store the Resources folder in the same directory in which you are running the scripts!

### API Key [IMPORTANT]
In order to automatically fetch the bazaar prices you'll need to provide your own Hypixel API key. To do this, simply hop into an in-game lobby, and type the following command:
```
/api
```
Copy the returned key, and save it in a file you should name `creds.txt` in the **Resources** folder (the fetchPrices.py script will need that file to authenticate your requests to the API).

### Running the Scipts
Great! Now that you have the prerequisites setup, all you need to do is fetch the bazaar prices by running the `fetchPrices.py` script first (this might take a while if you use the hypixel API), navigate to where you cloned this directory and run the following command. Note: use `fetchPrices2.py` if you would like to use the sky.lea.moe API.
```
python fetchPrices.py
```
Next, you can just run any comparison script you want!
```
python compareLevels.py
python compareFuels.py [minon level]
python compareTypes.py [minion level]
```
When running the Fuel and Type comparison tools, if you want to change the minion level, you can do so by adding an extra commandline argument when running the script. If no extra argument is input, the graphs will be generated for a max level minion. You can also change the fuel multiplier in the types comparator script by changing the fuel multiplyer variable.

### Outputs
The outputs should be immediately visible in the matplotlib viewer, but they are also saved in the **Raw Figs** folder as images.
The raw outputs from matplotlib have a bit of extra space around the graph, you might want to crop that out.

## Acknowledgements
Thanks to TBlazeWarriorT, I used a lot of the minion data from his famous spreadsheet, on top of painfully collecting my own.
Thanks to ThirtyVirus for providing the adequate situation in which I could release this tool.
If you spot any inconsistencies in the graphs or in the code, please let me know!!
