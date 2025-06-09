def eq(x, y, leeway = 0.1):
    Xlower = x - (x * leeway)
    Xupper = x + (x * leeway)
    if y > Xlower and y < Xupper:
        return True
    return False

def isDoji(candle):
    return eq(candle["Close"], candle["Close"]) and eq(candle["Open"], candle["Open"])

def isBullish(candle):
    return candle["Close"] > candle["Open"]

def isBearish(candle):
    return candle["Open"] > candle["Close"]

#Retourne
# 0 = rien faire
# 1 = Acheter
# -1 = Vendre
def decide(data, list = {}):
    candleM1 = data[-1]
    candleM2 = data[-2]
    candleM3 = data[-3]
    candleM4 = data[-4]
    candleM5 = data[-5]

    if isBearish(candleM2) and isBullish(candleM1) and candleM1["Open"] < candleM2["Close"] and candleM1["Close"] > candleM2["Open"]:
        return 1

    if isDoji(candleM1) and isBearish(candleM1):
        return -1


    #Detects Bearish Engulfing 72%
    if isBearish(candleM1) and isBullish(candleM2) and candleM1["Open"] > candleM2["Close"] and candleM1["Close"] < candleM2["Open"]:
        print("Bearish Engulfing")
        return -1
    # Detect Bearish Tweezer Top 61%
    if isBearish(candleM1) and isBullish(candleM2) and eq(candleM1["High"], candleM2["High"]) and eq(candleM1["Open"], candleM2["Close"]):
        print("Bearish Tweezer Top")
        return -1

    #Detect Bearing Evening Star 69%
    if isBullish(candleM3) and isBearish(candleM2) and isBearish(candleM1) and isDoji(candleM1):
        print("Bearing Evening Star")
        return -1

    """
    # Detect Bullish Kicker 68%
    if isBullish(candleM3) and isBearish(candleM4) and isBearish(candleM1) and candleM1["Open"] > (candleM2["Open"] + candleM2["Open"] * 0.05):
        print("Bullish Kicker")
        return 1
    #Detect Bullish Morning Star 65%
    if isDoji(candleM2) and isBullish(candleM1) and isBearish(candleM3) and isBullish(candleM2):
        print("Bullish Morning Star")
        return 1
    #Detect bullish engulfing 65%
    if isBearish(candleM2) and isBullish(candleM1) and candleM1["Open"] < candleM2["Close"] and candleM1["Close"] > candleM2["Open"]:
        print("bullish engulfing")
        return 1
    #Detect Bullish Tweezer Bottom 61%
    if isBearish(candleM2) and isBullish(candleM1) and eq(candleM1["Open"], candleM2["Close"]) and eq(candleM1["Low"], candleM2["Low"]):
        print("Bullish Tweezer Bottom")
        return 1
    #Detect Bullish Harami 54%
    if isBearish(candleM2) and isBearish(candleM3) and isBearish(candleM4) and isBullish(candleM1):
        print("Bullish Harami")
        return 1

    """

    return 0