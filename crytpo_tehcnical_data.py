import pandas_datareader as pdr
import matplotlib as plt
import mplfinance as mpf
import plotly as go
import datetime as dt

currency = 'USD'
start = dt.datetime(2017,1,1)
end = dt.datetime.now()

crytpo_ticker = 'BTC'
ticker_dates = []
ticker_highs = []
ticker_lows = []
ticker_closes = []
ticker_opens = []
ticker_volumes = []

crypto_data = pdr.DataReader(f'{crytpo_ticker}-{currency}', 'yahoo', start, end)

print(crypto_data)
def appending_crypto_data():
    for x in crypto_data:
        ticker_dates.append(crypto_data.index)
    for x in crypto_data:
        ticker_highs.append(crypto_data['High'])
    for x in crypto_data:
        ticker_lows.append(crypto_data['Low'])
    for x in crypto_data:
        ticker_opens.append(crypto_data['Open'])
    for x in crypto_data:
        ticker_closes.append(crypto_data['Close'])
    for x in crypto_data:
        ticker_volumes.append(crypto_data['Volume'])
appending_crypto_data()
# def plot_crypto_data():
#     fig = go.Figure(data=[go.Candlestick(x=ticker_dates,
#                                          open=ticker_opens,
#                                          high=ticker_highs,
#                                          low=ticker_lows,
#                                          close=ticker_closes)])
#
#     fig.show()
# plot_crypto_data()
