from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Global variables
asking_price = bidding_price = 0
total_quantity = int(round(random.uniform(0, 1), 2) * 10000) + 1000
random_number1 = random_number2 = random_number3 = 0.0
average_price = round(random_number1, 3)
selling_quantity = buy_value = buying_quantity = 0
last_done_price = total_quantity = gross_market_value = profit_loss = last_done_volume = 0

def generate_random_values():
    global random_number1, random_number2, random_number3
    global average_price, selling_quantity, buy_value, buying_quantity, bidding_price, asking_price
    global last_done_price, total_quantity, gross_market_value, profit_loss, last_done_volume

    while True:
        random_number1 = random.uniform(0, 1) * 2 + 3
        random_number2 = random.uniform(0, 1) * 2 + 3
        random_number3 = random.uniform(0, 1) * 2 + 3
        asking_price = round(random_number1, 3) * 5
        selling_quantity = int(round(random.uniform(0, 1), 2) * 10000) + 1000
        buy_value = round(random_number2, 3) * 5
        buying_quantity = int(round(random.uniform(0, 1), 2) * 10000) + 1000
        last_done_price = round(random_number3, 3) * 5
        gross_market_value = last_done_price * total_quantity
        profit_loss = gross_market_value - buy_value
        last_done_volume = int(round(random.uniform(0, 1), 2) * 10000) + 1000    
        print("Before")
        socketio.emit('new_values', {'sell_quantity': selling_quantity,
                                    'best_bid': buy_value, 
                                    'best_bid_quantity': buying_quantity, 
                                    'last_done_price': last_done_price, 
                                    'market_value': gross_market_value, 
                                    'profit_loss': profit_loss, 
                                    'last_done_volume': last_done_volume})
        print("After")
        time.sleep(5)

@app.route('/', methods=['GET'])
def home():
    return render_template('test.html')

if __name__ == '__main__':
    threading.Thread(target = generate_random_values).start()  # 5 seconds interval
    socketio.run(app, debug=True)