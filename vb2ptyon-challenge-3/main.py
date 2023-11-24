from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import threading
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)


global_values = {
    "asking_price": 0,
    "bidding_price": 0,
    "sell_quantity": 0,
    "bid_quantity": 0,
    "last_done_price": 0,
    "last_done_volume": 0,
    "average_price" : 1,
    "total_quantity": 0,
    "buy_value": 0,
    "market_value": 0,
    "profit_loss": 0
}

def initialiseGlobals():
    ranNum1 = random.random() * 2 + 3
    ranNum2 = random.random() * 2 + 3
    ranNum3 = random.random() * 2 + 3
    ranNum4 = random.random() * 2 + 3
    global_values["average_price"] = round(ranNum1, 3) * 5
    global_values["total_quantity"] = int(round(random.random(), 2) * 10000) + 1000
    global_values["buy_value"] = global_values["average_price"] * global_values["total_quantity"]
    global_values["asking_price"] = round(ranNum2, 3) * 5
    global_values["sell_quantity"] = int(round(random.random(), 2) * 10000) + 1000
    global_values["bidding_price"] = round(ranNum3, 3) * 5
    global_values["bid_quantity"] = int(round(random.random(), 2) * 10000) + 1000
    global_values["last_done_price"] = round(ranNum4, 3) * 5
    global_values["market_value"] = global_values["last_done_price"] * global_values["total_quantity"]
    global_values["profit_loss"] = global_values["market_value"] - global_values["buy_value"]
    global_values["last_done_volume"] = int(round(random.random(), 2) * 10000) + 1000
    socketio.emit('trade_data', global_values)  # Emit trade data


def update_global_values():
    while True:
        ranNum1 = random.random() * 2 + 3
        ranNum2 = random.random() * 2 + 3
        ranNum3 = random.random() * 2 + 3
        global_values["asking_price"] = round(ranNum1, 3) * 5
        global_values["sell_quantity"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["bidding_price"] = round(ranNum2, 3) * 5
        global_values["bid_quantity"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["last_done_price"] = round(ranNum3, 3) * 5
        global_values["market_value"] = global_values["last_done_price"] * global_values["total_quantity"]
        global_values["profit_loss"] = global_values["market_value"] - global_values["buy_value"]
        global_values["last_done_volume"] = int(round(random.random(), 2) * 10000) + 1000
        # print(global_values)
        socketio.emit('trade_data', global_values)  # Emit trade data
        time.sleep(5)  # Update every second



@app.route('/')
def index():
    return render_template('main.html')

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    global_values["order_quantity"] = int(data.get('OrderQuantity'))  # Order Quantity
    global_values["order_price"] = float(data.get('OrderPrice'))  # Order Price
    action = data.get('orderType')  # Buy or Sell
    print(action)

    if action == 'Buy' and global_values["buy_value"] >= 1000:
        global_values["average_price"] = (global_values["average_price"] * global_values["total_quantity"] + global_values["order_price"] * global_values["order_quantity"]) / (global_values["total_quantity"] + global_values["order_quantity"])
        global_values["total_quantity"] = global_values["total_quantity"] + global_values["order_quantity"]
        global_values["market_value"] = global_values["last_done_price"] * global_values["total_quantity"]
        global_values["buy_value"] = global_values["total_quantity"] * global_values["average_price"]
        global_values["profit_loss"] = global_values["market_value"] - global_values["buy_value"]
    elif action == 'Buy' and global_values["buy_value"] < 1000:
        return jsonify({"message": "You don't have enough fund to buy, reduce order"}), 400
    elif action == 'Sell' and global_values["total_quantity"] >= global_values["order_quantity"]:
        global_values["average_price"] = (global_values["average_price"] * global_values["total_quantity"] + global_values["order_price"] * global_values["order_quantity"]) / (global_values["total_quantity"] + global_values["order_quantity"])
        global_values["total_quantity"] = global_values["total_quantity"] - global_values["order_quantity"]
        global_values["market_value"] = global_values["last_done_price"] * global_values["total_quantity"]
        global_values["buy_value"] = global_values["total_quantity"] * global_values["average_price"]
        global_values["profit_loss"] = global_values["market_value"] - global_values["buy_value"]
    elif action == 'Sell' and global_values["total_quantity"] < global_values["order_quantity"]:
        return jsonify({"message": "Not enough shares, reduce order"}), 400
    else:
        return jsonify({"message": "Invalid action or not enough quantity to sell"}), 400
    socketio.emit('trade_data', global_values)



if __name__ == '__main__':
    initialiseGlobals()
    threading.Thread(target=update_global_values).start()
    socketio.run(app, debug=True)