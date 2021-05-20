import pandas_datareader as pdr
import matplotlib as plt
import mplfinance as mpf
import plotly as go
import datetime as dt
import pandas as pd

currency = 'USD'
start = dt.datetime(2009,1,1)
end = dt.datetime.now()

userTicker = input('Enter a ticker for a crypto in lowercase to \n generate a data frame'
                   ' and to generate info about the crypto: ')

crytpo_ticker = userTicker.upper().strip()
ticker_dates = []
ticker_highs = []
ticker_lows = []
ticker_closes = []
ticker_opens = []
ticker_volumes = []

crypto_data = pdr.DataReader(f'{crytpo_ticker}-{currency}', 'yahoo', start, end)
# Appending the data to lists
def appending_crypto_data():
    global ticker_highs, ticker_lows, ticker_opens, ticker_closes, ticker_dates, ticker_volumes
    for x in crypto_data:
        ticker_dates = (crypto_data.index)
    for x in crypto_data:
        ticker_highs = (crypto_data['High'])
    for x in crypto_data:
        ticker_lows = (crypto_data['Low'])
    for x in crypto_data:
        ticker_opens = (crypto_data['Open'])
    for x in crypto_data:
        ticker_closes = (crypto_data['Close'])
    for x in crypto_data:
        ticker_volumes = (crypto_data['Volume'])
appending_crypto_data()

def moving_averages(x):
    # Simple moving averages
    global five_day_SMA,ten_day_SMA,twenty_day_SMA,fifty_day_SMA,one_hundred_day_SMA,two_hundred_day_SMA
    five_day_SMA = ticker_closes.rolling(5, min_periods=1).mean()
    ten_day_SMA = ticker_closes.rolling(10, min_periods=1).mean()
    twenty_day_SMA = ticker_closes.rolling(20, min_periods=1).mean()
    fifty_day_SMA = ticker_closes.rolling(50, min_periods=1).mean()
    one_hundred_day_SMA = ticker_closes.rolling(100, min_periods=1).mean()
    two_hundred_day_SMA = ticker_closes.rolling(200, min_periods=1).mean()
    # Exponential moving averages
    five_day_EMA = pd.Series.ewm(ticker_closes, span=5).mean()
    ten_day_EMA = pd.Series.ewm(ticker_closes, span=10).mean()
    eight_day_EMA = pd.Series.ewm(ticker_closes, span=8).mean()
    twelve_day_EMA = pd.Series.ewm(ticker_closes, span=12).mean()
    twenty_day_EMA = pd.Series.ewm(ticker_closes, span=20).mean()
    twenty_six_day_EMA = pd.Series.ewm(ticker_closes, span=26).mean()
    fifty_day_EMA = pd.Series.ewm(ticker_closes, span=50).mean()
    one_hundred_day_EMA = pd.Series.ewm(ticker_closes, span=100).mean()
    two_hundred_day_EMA = pd.Series.ewm(ticker_closes, span=200).mean()
moving_averages(crytpo_ticker)

print(five_day_SMA[-1])
print(twenty_day_SMA[-1])
print(fifty_day_SMA[-1])
print(one_hundred_day_SMA[-1])
print(two_hundred_day_SMA[-1])