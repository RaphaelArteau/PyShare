from flask import Flask, jsonify
import os

from stock import Stock

app = Flask(__name__)
stocks = {}

@app.route('/stocks', methods=['GET'])
def getStocks(timestamp):
    return jsonify(list(stocks.keys()))

@app.route('/gains/<string:timestamp>', methods=['GET'])
def getGains(timestamp):
    ret = {}
    for ticket in stocks:
        stock = stocks[ticket]
        ret[stock.stock] = stock.gains(timestamp)
    return jsonify(ret)

@app.route('/stock/<string:stock>/<string:timestamp>', methods=['GET'])
def getStockInfo(stock, timestamp):
    ret = stocks[stock].info(timestamp)
    return jsonify(ret)

if __name__ == '__main__':
    subfolders = [f.path for f in os.scandir("Stocks") if f.is_dir()]
    for subfolder in subfolders:
        s = Stock(subfolder)
        stocks[s.stock] = s
    app.run(debug=True)