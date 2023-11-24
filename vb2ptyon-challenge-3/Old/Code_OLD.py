from flask import Flask, render_template, request, jsonify
import random
import threading
import time

app = Flask(__name__)

global_values = {
    "Asking Price": 0,
    "SQ": 0,
    "BD": 0,
    "BQ": 0,
    "LP": 0,
    "MV": 0,
    "PL": 0,
    "LVOL": 0,
    "TQ": 0,
    "BV": 0
}

def update_global_values():
    while True:
        ranNum1 = random.random() * 2 + 3
        ranNum2 = random.random() * 2 + 3
        ranNum3 = random.random() * 2 + 3
        global_values["Asking Price"] = round(ranNum1, 3) * 5
        global_values["SQ"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["BD"] = round(ranNum2, 3) * 5
        global_values["BQ"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["LP"] = round(ranNum3, 3) * 5 # Last Done Price
        global_values["MV"] = global_values["LP"] * global_values["TQ"] # Market Value
        global_values["PL"] = global_values["MV"] - global_values["BV"]
        global_values["LVOL"] = int(round(random.random(), 2) * 10000) + 1000 # Last Done Volume
        time.sleep(1) # update every second

@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    OrderQuantity = int(data.get('OrderQuantity'))  # Order Quantity
    OrderPrice = float(data.get('OrderPrice'))  # Order Price
    action = data.get('action')  # Buy or Sell

    if action == 'Buy' and BuyValue >= 1000:
        AveragePrice = (AveragePrice * TotalNumberOfSharesInHand + OrderPrice * OrderQuantity) / (TotalNumberOfSharesInHand + OrderQuantity)
        TotalNumberOfSharesInHand = TotalNumberOfSharesInHand + OrderQuantity
        GrossMarketValue = LastDonePrice * TotalNumberOfSharesInHand
        BuyValue = TotalNumberOfSharesInHand * AveragePrice
        ProfitOrLoss = GrossMarketValue - BuyValue
    elif action == 'Buy' and BuyValue < 1000:
        return jsonify({"message": "You don't have enough fund to buy, reduce order"}), 400
    elif action == 'Sell' and TotalNumberOfSharesInHand >= OrderQuantity:
        AveragePrice = (AveragePrice * TotalNumberOfSharesInHand + OrderPrice * OrderQuantity) / (TotalNumberOfSharesInHand + OrderQuantity)
        TotalNumberOfSharesInHand = TotalNumberOfSharesInHand - OrderQuantity
        GrossMarketValue = LastDonePrice * TotalNumberOfSharesInHand
        BuyValue = TotalNumberOfSharesInHand * AveragePrice
        ProfitOrLoss = GrossMarketValue - BuyValue
    else:
        return jsonify({"message": "Invalid action or not enough quantity to sell"}), 400

    return jsonify({
        'AveragePrice': format(global_values["AP"], '.2f'),
        'TotalQuantity': global_values["TQ"],
        'BuyValue': format(global_values["BV"], '.2f'),
        'AskingPrice': format(global_values["AP"], '.2f'),
        'SellQuantity': global_values["SQ"],
        'BiddingPrice': format(global_values["BD"], '.2f'),
        'BidQuantity': global_values["BQ"],
        'LastDonePrice': format(global_values["LP"], '.2f'),
        'MarketValue': format(global_values["MV"], '.2f'),
        'ProfitLoss': format(global_values["PL"], '.2f'),
        'LastDoneVolume': global_values["LVOL"]
    })

if __name__ == '__main__':
    threading.Thread(target=update_global_values).start()
    app.run(debug=True)