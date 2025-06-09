PyShare is a simple strategy backtester for day or swing trading. 

Pyshare contains 3 different folders : 
- PyShare+Tester : Uses the market API to test a strategy. You can add your own strategies under the strategies subfolder. Each strategy needs a decide method that will choose if it buys (returns 1), sells (returns -1) a stock or does nothing (returns 0)
- PyShare-ContentGetter : The getter uses yFinance to retrieve the data from a specified stock and a specified interval. It stores the content in subfolder with the stock as folder name
- MarketAPI : An API to run along the tester. It loads the stock folders found under the Stocks subfolder and serves them to the tester
