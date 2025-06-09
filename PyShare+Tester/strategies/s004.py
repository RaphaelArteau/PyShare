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


def isVolumeSpike(candle, avg_volume):
    return candle["Volume"] > avg_volume * 1.5

def isUptrend(data):
    return data[-1]["Close"] > data[-2]["Close"] > data[-3]["Close"]

def isDowntrend(data):
    return data[-1]["Close"] < data[-2]["Close"] < data[-3]["Close"]

def decide(data, list={}):
    avg_volume = sum(candle["Volume"] for candle in data[-10:]) / 10  # Average volume over the last 10 candles
    candleM1 = data[-1]
    candleM2 = data[-2]
    candleM3 = data[-3]

    # Buy signals
    # Bullish reversal pattern with volume spike
    if isBearish(candleM3) and isDoji(candleM2) and isBullish(candleM1) and isVolumeSpike(candleM1, avg_volume):
        print("Bullish Reversal with Volume Spike")
        return 1

    # Strong uptrend continuation with volume support
    if isUptrend(data) and isVolumeSpike(candleM1, avg_volume):
        print("Uptrend Continuation with Volume Spike")
        return 1

    # Sell signals
    # Bearish reversal pattern with volume spike
    if isBullish(candleM3) and isDoji(candleM2) and isBearish(candleM1) and isVolumeSpike(candleM1, avg_volume):
        print("Bearish Reversal with Volume Spike")
        return -1

    # Strong downtrend continuation with volume support
    if isDowntrend(data) and isVolumeSpike(candleM1, avg_volume):
        print("Downtrend Continuation with Volume Spike")
        return -1

    return 0