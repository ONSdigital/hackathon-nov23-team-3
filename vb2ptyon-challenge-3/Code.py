from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

global_values = {
    "asking_price": 0,
    "sell_quantity": 0,
    "bidding_price": 0,
    "bid_quantity": 0,
    "last_done_price": 0,
    "last_done_volume": 0,
    "action"    : "Buy",        # Buy or Sell
    "order_quantity"  : 0,            # Quantity to buy or sell
    "order_price"  : 0,            # Quantity to buy or sell
    "average_price" : 0,
    "total_quantity": 0,
    "buy_value": 0,
    "market_value": 0,
    "profit_loss": 0
}

def update_global_values():
    while True:
        global_values["asking_price"] = round(random.random() * 2 + 3, 3) * 5
        global_values["sell_quantity"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["bidding_price"] = round(random.random() * 2 + 3, 3) * 5
        global_values["bid_quantity"] = int(round(random.random(), 2) * 10000) + 1000
        global_values["last_done_price"] = round(random.random() * 2 + 3, 3) * 5
        global_values["market_value"] = global_values["last_done_price"] * global_values["total_quantity"]
        global_values["profit_loss"] = global_values["market_value"] - global_values["buy_value"]
        global_values["last_done_volume"] = int(round(random.random(), 2) * 10000) + 1000
        socketio.emit('trade_data', global_values)  # Emit trade data
        time.sleep(1)  # Update every second

@app.route('/')
def index():
    return render_template('trade.html')


if __name__ == '__main__':
    threading.Thread(target=update_global_values).start()
    socketio.run(app, debug=True)