We shall use the following variables to represent the aforementioned data:

AP- Asking Price
BD- Bidding Price
SQ- Selling Quantity
BQ- Buying Quantity
LP- Last Done Price
OP- Order Price
OQ- Order Quantity
AVP- Average Price
BV- Buy Value
MV- Gross Market Value
TQ- Total Number of Shares in Hand

In this program, we need to insert a timer to generate random values for the Asking Price, the Bidding Price, the Selling Quantity, the Buying Quantity and the Last Done Price. You can set the timer to any interval you think is suitable, here we set it to 15 seconds so that the values changes every 15 seconds to simulate the real stock market. The code is as follows:

ranNum1 = Rnd() * 2 + 3
ranNum2 = Rnd() * 2 + 3
ranNum3 = Rnd() * 2 + 3
AP = Round(ranNum1, 3) * 5
SQ = Int(Round(Rnd(), 2) * 10000) + 1000
BD = Round(ranNum2, 3) * 5
BQ = Int(Round(Rnd(), 2) * 10000) + 1000
LP = Round(ranNum3, 3) * 5 ‘Last Done Price
LVOL = Int(Round(Rnd(), 2) * 10000) + 1000 ‘Last Done Volume
PL- Profit or Loss

Besides that, we need to write code to calculate the Average Price, the Buy Value, the Gross Market Value and the total number of shares in hand, as follows:

AVP = (AVP * TQ + OP * OQ) / (TQ + OQ)
TQ = TQ + OQ
MV = LP * TQ
BV = TQ * AVP

