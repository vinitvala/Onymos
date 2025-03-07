import random

# Constants mentioned in the question
MAX_TICKERS = 1024
MAX_ORDERS_PER_TICKER = 10000

# We represent tickers by a simple integer index

def get_ticker_index(symbol):
    """
    This is a simple function to map a ticker symbol to a number [from 0 to 1023]
    Used a Naive approach that basically sums character codes and takes % 1024.
    """
    s = 0
    for ch in symbol:
        s += ord(ch)
    return s % MAX_TICKERS


# Each ticker has two lists:
#   - buyOrders[tickerIndex]:  list of (price, quantity) for Buy orders, sorted by descending price
#   - sellOrders[tickerIndex]: list of (price, quantity) for Sell orders, sorted by ascending price

# Storing them in global arrays for simplicity.
# Not using shared locks here for now.

buyOrders  = [[] for _ in range(MAX_TICKERS)]
sellOrders = [[] for _ in range(MAX_TICKERS)]

def addOrder(orderType, tickerSymbol, quantity, price):
    """
    Inserts an order (Buy or Sell) into the global order book.
      orderType : "Buy" or "Sell"
      tickerSymbol: e.g. "AAPL"
      quantity : integer
      price : float or integer
    """
    tickerIndex = get_ticker_index(tickerSymbol)
    if tickerIndex < 0 or tickerIndex >= MAX_TICKERS:
        return  # ignore bad ticker index

    # For Buy, list sorted in descending order.
    # For Sell, list sorted in ascending order.
    if orderType == "Buy":

        arr = buyOrders[tickerIndex]
        # Inserting new order at the correct position.
        n = len(arr)
        inserted = False
        for i in range(n):
            if price >= arr[i][0]:
                arr.insert(i, (price, quantity))
                inserted = True
                break
        if not inserted:
            arr.append((price, quantity))

    else:
        # orderType == "Sell"
        arr = sellOrders[tickerIndex]
        n = len(arr)
        inserted = False
        for i in range(n):
            if price <= arr[i][0]:
                arr.insert(i, (price, quantity))
                inserted = True
                break
        if not inserted:
            arr.append((price, quantity))

def matchOrder(tickerSymbol):
    """
    Matches all possible Buy & Sell orders for the given ticker

    Because buyOrders are sorted descending, and sellOrders are sorted ascending,
    we can match in one forward pass.
    """
    tickerIndex = get_ticker_index(tickerSymbol)
    bList = buyOrders[tickerIndex]
    sList = sellOrders[tickerIndex]

    i = 0  # pointer for bList
    j = 0  # pointer for sList

    # Accumulating the new states in-place to reduce matched orders.

    while i < len(bList) and j < len(sList):
        bPrice, bQty = bList[i]
        sPrice, sQty = sList[j]

        # If a match is possible
        if bPrice >= sPrice:
            # Determine how much we can match
            matchedQty = bQty if bQty < sQty else sQty

            # Update quantities
            bQty -= matchedQty
            sQty -= matchedQty

            # If the buy order is fully filled, remove it
            if bQty == 0:
                # remove bList[i]
                bList.pop(i)
                # do NOT increment i, because list just shrank
            else:
                # partially filled
                bList[i] = (bPrice, bQty)
                # move to next buy
                i += 1

            # If the sell order is fully filled, remove it
            if sQty == 0:
                sList.pop(j)
                # do NOT increment j, because list just shrank
            else:
                # partially filled
                sList[j] = (sPrice, sQty)
                # move to next sell
                j += 1

        else:
            # No match is possible here, so move on.
            # Because buy[i].price < sell[j].price, that buy won't match any
            # further sells either.
            # So move to the next buy order.
            i += 1

############################################
# SIMULATION WRAPPER
############################################

def simulateRandomOrders(numOrders=20):
    """
    Demonstrates random stock transactions using addOrder.
    Then we call matchOrder on each ticker we used.
    """
    # We'll pick from a small set of mock ticker symbols to show how it might work
    tickers = ["ONYM", "AAPL", "TSLA", "GOOG", "MSFT"]  # and so on

    used_ticker_symbols = []

    for _ in range(numOrders):
        tkr = random.choice(tickers)
        used_ticker_symbols.append(tkr)
        oType = "Buy" if random.randint(0, 1) == 0 else "Sell"
        qty   = random.randint(1, 50)
        # We'll pick random price in a small range
        prc   = random.randint(90, 110)

        addOrder(oType, tkr, qty, prc)

    # Now match each ticker we touched
    for tkr in set(used_ticker_symbols):
        matchOrder(tkr)

    # To check to see leftover buy/sell orders after matching:
    # for tkr in set(used_ticker_symbols):
    #     idx = get_ticker_index(tkr)
    #     print(tkr, "BUY:", buyOrders[idx])
    #     print(tkr, "SELL:", sellOrders[idx])

############################################
# DEMO MAIN
############################################

def main():
    # Example usage
    # Add a few manual orders
    addOrder("Buy", "AAPL", 10, 100)
    addOrder("Sell", "AAPL", 5,  98)
    addOrder("Sell", "AAPL", 5,  101)
    
    # Match them
    matchOrder("AAPL")

    # Random simulation
    simulateRandomOrders(numOrders=10)

if __name__ == "__main__":
    main()

