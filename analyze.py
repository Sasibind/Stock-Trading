import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Replace these with your PostgreSQL connection details
db_params = {
   'host': '127.0.0.1',
   'port' : '5432',
   'database': 'stock_data',
   'user': 'postgres',
   'password': 'password'
}

# Connect to the PostgreSQL database
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

# SQL query to fetch trading data from the table
query = "SELECT date, close FROM aapl ORDER BY date;"

# Read data into a Pandas DataFrame
df = pd.read_sql(query, engine, index_col="date", parse_dates=True)

# Calculate the required moving averages
df["50_day_sma"] = df["close"].rolling(window=50).mean()
df["500_day_sma"] = df["close"].rolling(window=500).mean()
df["20_day_sma"] = df["close"].rolling(window=20).mean()
df["200_day_sma"] = df["close"].rolling(window=200).mean()
df["10_day_sma"] = df["close"].rolling(window=10).mean()
df["5_day_sma"] = df["close"].rolling(window=5).mean()

# Generate buy and sell signals based on crossovers
df["buy_signal"] = (df["50_day_sma"] > df["500_day_sma"]) & (df["50_day_sma"].shift(1) <= df["500_day_sma"].shift(1))
df["sell_signal"] = (df["20_day_sma"] < df["200_day_sma"]) & (df["20_day_sma"].shift(1) >= df["200_day_sma"].shift(1))

# Close buy positions
df["close_buy_positions"] = (df["10_day_sma"] > df["20_day_sma"]) & (df["10_day_sma"].shift(1) <= df["20_day_sma"].shift(1))

# Close sell positions
df["close_sell_positions"] = (df["5_day_sma"] > df["10_day_sma"]) & (df["5_day_sma"].shift(1) <= df["10_day_sma"].shift(1))

# Plot the data with buy signals
plt.figure(figsize=(10, 6))
plt.plot(df.index, df["close"], label="Close Price")
plt.plot(df.index, df["50_day_sma"], label="50-day SMA")
plt.plot(df.index, df["500_day_sma"], label="500-day SMA")

plt.scatter(df[df["buy_signal"]].index, df[df["buy_signal"]]["50_day_sma"], marker="^", color="g", label="Buy Signal")

plt.title("Trading Data with Buy Signals")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

# Plot the data with sell signals
plt.figure(figsize=(10, 6))
plt.plot(df.index, df["close"], label="Close Price")
plt.plot(df.index, df["20_day_sma"], label="20-day SMA")
plt.plot(df.index, df["200_day_sma"], label="200-day SMA")

plt.scatter(df[df["sell_signal"]].index, df[df["sell_signal"]]["20_day_sma"], marker="v", color="r", label="Sell Signal")

plt.title("Trading Data with Sell Signals")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

# Close the database connection
engine.close()