import pandas as pd
from database import get_db_connection

def moving_average_crossover_strategy(short_window: int = 10, long_window: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT datetime, close FROM ticker_data ORDER BY datetime ASC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"message": "No data available"}

    df = pd.DataFrame(rows, columns=["datetime", "close"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)

    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window=long_window).mean()

    df["signal"] = 0
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1 
    df.loc[df["short_ma"] < df["long_ma"], "signal"] = -1 

    initial_capital = 10000
    shares_held = 0
    cash = initial_capital
    trade_log = []

    for i in range(1, len(df)):
        if df["signal"].iloc[i] == 1 and df["signal"].iloc[i - 1] != 1:  # Buy
            shares_held = cash / df["close"].iloc[i]
            cash = 0
            trade_log.append({"datetime": df.index[i], "action": "BUY", "price": df["close"].iloc[i]})
        
        elif df["signal"].iloc[i] == -1 and df["signal"].iloc[i - 1] != -1:  # Sell
            cash = shares_held * df["close"].iloc[i]
            shares_held = 0
            trade_log.append({"datetime": df.index[i], "action": "SELL", "price": df["close"].iloc[i]})

    final_value = cash + (shares_held * df["close"].iloc[-1])

    return {
        "initial_capital": initial_capital,
        "final_value": final_value,
        "return_percentage": ((final_value - initial_capital) / initial_capital) * 100,
        "trades": trade_log
    }
