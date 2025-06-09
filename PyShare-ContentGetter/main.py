from operator import truediv

import yfinance as yf
import pandas as pd
import time
import os
from datetime import datetime, date, timedelta

__STOCK__ = "HUT.TO"
__PATH__ = __STOCK__ + "/1m"

startDate = datetime.now() - timedelta(days=29)
startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)


ticket = yf.Ticker(__STOCK__)


prevhistory = ticket.history(interval="60m", period="max")

#prevhistory = ticket.history(interval="1m", start=startDate, end=startDate + timedelta(days=5)).reset_index()
cont = True
while cont:
    time.sleep(10)
    prevDate = startDate
    startDate = prevhistory["Datetime"][len(prevhistory["Datetime"]) - 1]
    startDate = startDate.to_pydatetime().replace(tzinfo=None)
    startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
    startDate = startDate + timedelta(days=1)
    endDate = startDate + timedelta(days=5)
    if endDate > datetime.now() :
        endDate = datetime.now()
        endDate = endDate.replace(hour=0, minute=0, second=0, microsecond=0)
        endDate = endDate + timedelta(days=1)
        cont = False
    history = ticket.history(interval="1m", start=startDate, end=endDate).reset_index()
    prevhistory = pd.concat([prevhistory, history], ignore_index=True)
prevhistory = prevhistory.set_index("Datetime")


if not os.path.exists(__PATH__):
    os.makedirs(__PATH__)

__PATH__ += "/data.csv"

prevhistory.to_csv(__PATH__, sep="|")
