# For the SWE position at Onymos Inc.

# Onymos Stock Trading Engine

This project implements a simplified, real-time stock trading engine in **Python**. It provides two main functions:

1. **`addOrder(orderType, tickerSymbol, quantity, price)`**  
   - Adds new Buy/Sell orders to the order book (without using dictionaries/maps).  
   - Buy orders are kept in descending price order, sell orders in ascending price order.

2. **`matchOrder(tickerSymbol)`**  
   - Matches all possible Buy and Sell orders in **O(n)** time for the specified ticker.

## Run the script:
python onymos.py


Thank you!
