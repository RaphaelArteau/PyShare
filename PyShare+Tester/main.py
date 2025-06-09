from datetime import datetime, timedelta
import requests
import time
import json as JSON
from strategies.s004 import decide

__MARKET_OPEN__ = 34500
__MARKET_CLOSE__ = 57300
__TOTAL__ = 0
#day = datetime.now().replace(year=2024, month=11, day=29, hour=0, minute=0, second=0, microsecond=0)
day = datetime.now().replace(year=2024, month=11, day=29, hour=0, minute=0, second=0, microsecond=0)
clock = day
end = datetime.now().replace(year=2024, month=12, day=22, hour=0, minute=0, second=0, microsecond=0)

while day < end:
    while day.weekday() >= 5:
        day += timedelta(days=1)
    boughtList = {}
    watchlist = []
    clock = day + timedelta(seconds=__MARKET_OPEN__)
    close = day + timedelta(seconds=__MARKET_CLOSE__)
    while clock < close:

        top = requests.get("http://127.0.0.1:5000/gains/"+str(int(clock.timestamp())))
        json = JSON.loads(top.text)
        for item in json:
            if json[item] > 0.03 and item not in watchlist:
                watchlist.append(item)
                boughtList[item] = {
                    "availableFunds" : 1000,
                    "previousFunds" : 0,
                    "availableToSell" : 0
                }

        for watch in watchlist:
            data = requests.get("http://127.0.0.1:5000/stock/"+str(watch)+"/"+str(int(clock.timestamp())))
            data = JSON.loads(data.text)
            d = decide(data, list = boughtList[watch])
            if clock + timedelta(minutes=1) >= close:
                d = -1
            if d == 1:
                if boughtList[watch]["availableToSell"] == 0:
                    print("---------------------")
                    print(clock.strftime('%m/%d/%Y %H:%M'))
                    boughtList[watch]["previousFunds"] = boughtList[watch]["availableFunds"]
                    print("Bought "+watch+" for "+str(data[-1]["Close"]))
                    quantityBought = boughtList[watch]["availableFunds"] / data[-1]["Close"]
                    boughtList[watch]["availableFunds"] = 0
                    boughtList[watch]["availableToSell"] = quantityBought
            elif d == -1:
                print("---------------------")
                print(clock.strftime('%m/%d/%Y %H:%M'))
                if boughtList[watch]["availableToSell"] > 0:
                    value = boughtList[watch]["availableToSell"] * data[-1]["Close"]
                    earn = value / boughtList[watch]["previousFunds"]
                    if earn < 1:
                        print("Sold "+watch+" for "+str(data[-1]["Close"])+" with a lost of "+str(1-earn))
                    else:
                        print("Sold "+watch+" for "+str(data[-1]["Close"])+" with a earning of "+str(earn-1))
                    boughtList[watch]["availableFunds"]  = value
                    boughtList[watch]["previousFunds"] = 0
                    boughtList[watch]["availableToSell"]  = 0
        clock = clock + timedelta(minutes=1)
        #time.sleep(0.2)
    day = day + timedelta(days=1)
    print("----------------------------")
    print("End of day")
    for watch in watchlist:
        __TOTAL__ += boughtList[watch]["availableFunds"] - 1000
        print(watch + " Earning : "+str(boughtList[watch]["availableFunds"] - 1000) + " Return : " + str(( boughtList[watch]["availableFunds"] - 1000) / 1000))
    print("Total profit: "+str(__TOTAL__))
    #time.sleep(20)

