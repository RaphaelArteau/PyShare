import pandas as pd
import datetime

class Stock:

    def __init__(self, path):
        self.data = pd.read_csv(path+"/1m/data.csv", sep="|").set_index("Datetime")
        self.stock = path.split("/")[1]
        self.days = {}
        for i in range(len(self.data.index)):
            date = datetime.datetime.fromisoformat(self.data.index[i])
            if i == 0 :
                lastDate = date.day
                self.days[date] = 0
                continue
            if date.day != lastDate:
                lastDate = date.day
                self.days[date] = i
        self.gains(1733938420)



    def gains(self, timestamps):
        openingIndex = self.days[self.indexStartOfDay(timestamps)]
        infoOpening = self.data.iloc[openingIndex]
        lastestIndex = self.closestTimeStamp(timestamps, opening = openingIndex)
        infoLatest = self.data.iloc[lastestIndex]
        return ( infoLatest["Close"]  -  infoOpening["Open"]) / infoOpening["Open"]

    def info(self, timestamps):
        time = datetime.datetime.fromtimestamp(int(timestamps))
        ret = []
        openingIndex = self.days[self.indexStartOfDay(timestamps)]
        for i in range(openingIndex, len(self.data.index)):
            ret.append(self.data.iloc[i].to_dict())
            date = datetime.datetime.fromisoformat(self.data.index[i])
            if date.replace(tzinfo=None) >= time: break
        return ret

    def indexStartOfDay(self, time):
        time = datetime.datetime.fromtimestamp(int(time))
        timestamps = list(self.days.keys())
        left, right = 0, len(timestamps) - 1
        while left <= right:
            mid = (left + right) // 2
            if timestamps[mid].replace(tzinfo=None) == time:
                result = mid
                break
            elif timestamps[mid].replace(tzinfo=None) < time:
                result = mid  # Record this as the closest smaller index
                left = mid + 1  # Search the right half for possibly closer results
            else:
                right = mid - 1  # Search the left half for smaller elements

        return timestamps[result]




    def closestTimeStamp(self, time, opening = None):
        if opening is None:
            opening = self.days[self.indexStartOfDay(time)]
        time = datetime.datetime.fromtimestamp(int(time))
        ret = -1
        for i in range(opening, len(self.data.index)):
            date = datetime.datetime.fromisoformat(self.data.index[i])
            if date.replace(tzinfo=None) == time:
                return i
            elif date.replace(tzinfo=None) > time:
                return i-1
        return ret

