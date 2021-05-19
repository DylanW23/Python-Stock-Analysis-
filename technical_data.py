import pandas_datareader as pdr
from datetime import date
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from tkinter import *
import yfinance as yf
import mplfinance as mpf
import pprint
import plotly.graph_objects as go

today = date.today()
startDate = "2020-01-01"
# Function for letting the user grab data from yfinance
def grabDataYahooFinance(x):
    # User input and passing it to yfinance
    ticker = userTicker.strip().upper()
    data = yf.Ticker(x)
    yahooFinanceTicker = yf.Ticker(ticker)
    dataFrame = pdr.get_data_yahoo(ticker, start=startDate, end=today)
    # Daily closes for the total lifetime of a stock
    max_daily_intervals = data.history(period='max', interval='1d')
    # Candlestick data
    max_daily_closes = (max_daily_intervals['Close'])
    max_daily_opens = max_daily_intervals['Open']
    max_daily_lows = max_daily_intervals['Low']
    max_daily_highs = max_daily_intervals['High']
    # A list of the daily volumes for total lifetime of stock
    max_daily_volumes = (max_daily_intervals['Volume'])
    # List of the dates of for the lifetime of the stock
    max_daily_intervals_dates = max_daily_intervals.index
    # Yesterdays close of the stock price
    yesterdays_close = max_daily_closes[-1]
    # Year to date period, daily closes
    # This is used to calculate the ytd moving average
    ytd_daily_intervals = data.history(period="ytd", interval='1d')
    ytd_daily_closes = ytd_daily_intervals['Close']
    ytd_daily_volume = ytd_daily_intervals['Volume']
    ytd_intervals_dates = ytd_daily_intervals.index

    # Function to generate stock data using yfinance
    def generateStockData(x):
        global long_business_summary
        ticker = x.strip().upper()
        yfTicker = yf.Ticker(ticker)
        Info = yfTicker.info
        Dividends = yfTicker.dividends
        Actions = yfTicker.actions
        Splits = yfTicker.splits
        Financials = yfTicker.financials
        major_holders = yfTicker.major_holders
        instituional_holders = yfTicker.institutional_holders
        Recomendations = yfTicker.recommendations
        stock_long_name = Info['longName']
        long_business_summary = Info['longBusinessSummary']
        beta = Info['beta']
        fifty_two_week_high = Info['fiftyTwoWeekHigh']
        fifty_two_week_low = Info['fiftyTwoWeekLow']
        forward_stock_EPS = Info['forwardEps']
        forward_stock_PE = Info['forwardPE']
        trailing_stock_EPS = Info['trailingEps']
        trailing_stock_PE = Info['trailingPE']

        pprint.pprint(Info)
        pprint.pprint(Financials)
        pprint.pprint(major_holders)
        pprint.pprint(instituional_holders)


    def create_tkinter():
        # Functions
        def calc_moving_averages(x):
            # SMA DATA
            global five_day_SMA, ten_day_SMA, twenty_day_SMA, fifty_day_SMA, one_hundred_day_SMA, two_hundred_day_SMA, ytd_SMA
            five_day_SMA = max_daily_closes.rolling(5, min_periods=1).mean()
            ten_day_SMA = max_daily_closes.rolling(10, min_periods=1).mean()
            twenty_day_SMA = max_daily_closes.rolling(20, min_periods=1).mean()
            fifty_day_SMA = max_daily_closes.rolling(50, min_periods=1).mean()
            one_hundred_day_SMA = max_daily_closes.rolling(100, min_periods=1).mean()
            two_hundred_day_SMA = max_daily_closes.rolling(200, min_periods=1).mean()
            ytd_SMA = ytd_daily_closes.rolling(365, min_periods=1).mean()
            # EMA DATA
            global five_day_EMA, ten_day_EMA, eight_day_EMA, twelve_day_EMA, twenty_day_EMA, twenty_six_day_EMA, fifty_day_EMA, two_hundred_day_EMA, one_hundred_day_EMA
            dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
            five_day_EMA = pd.Series.ewm(max_daily_closes, span=5).mean()
            ten_day_EMA = pd.Series.ewm(max_daily_closes, span=10).mean()
            eight_day_EMA = pd.Series.ewm(max_daily_closes, span=8).mean()
            twelve_day_EMA = pd.Series.ewm(max_daily_closes, span=12).mean()
            twenty_day_EMA = pd.Series.ewm(max_daily_closes, span=20).mean()
            twenty_six_day_EMA = pd.Series.ewm(max_daily_closes, span=26).mean()
            fifty_day_EMA = pd.Series.ewm(max_daily_closes, span=50).mean()
            one_hundred_day_EMA = pd.Series.ewm(max_daily_closes, span=100).mean()
            two_hundred_day_EMA = pd.Series.ewm(max_daily_closes, span=200).mean()

            # MatPlotLob Plots DATA
            def plot_SMA_data():
                rcParams['figure.figsize'] = 12, 6
                plt.grid(True, color='k', linestyle=":")
                plt.xlabel("Date")
                plt.ylabel("Price")
                plt.title(ticker + " SMAs, 3 month Time Frame")
                plt.plot(max_daily_intervals_dates[-90:], max_daily_closes[-90:], label="YTD Closes")
                # plt.plot(ytd_intervals_dates, ytd_SMA, label="YTD SMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], twenty_day_SMA[-90:], label="20 SMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], fifty_day_SMA[-90:], label="50 SMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], two_hundred_day_SMA[-90:], label="200 SMA", linestyle="--")
                plt.legend()
                plt.show()
            # Plotly Plot Data
            def plotly_plot_SMA():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=max_daily_closes[-90:], name='20-SMA',
                                          line=dict(color='#f3722c', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=twenty_day_SMA[-90:], name='20-SMA',
                                          line=dict(color='#f3722c', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=fifty_day_SMA[-90:], name='50-SMA',
                                          line=dict(color='#f9c74f', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=five_day_SMA[-90:], name='5-SMA',
                                          line=dict(color='#90be6d', width=4, dash='doth')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=one_hundred_day_SMA[-90:], name='100-SMA',
                                          line=dict(color='#577590', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=two_hundred_day_SMA[-90:], name='200-SMA',
                                          line=dict(color='#277da1', width=4, dash='dot')))

                fig.update_layout(title=ticker + ' - SMA Data',
                                  xaxis_title='Date',
                                  yaxis_title='Dollars')

                fig.show()
            # Matplotlob Plot Data
            def plot_EMA_data():
                rcParams['figure.figsize'] = 12, 6
                plt.grid(True, color='k', linestyle=":")
                plt.xlabel("Date")
                plt.ylabel("Price")
                plt.title(ticker + " EMAs, 3 Month Time Frame")
                plt.plot(max_daily_intervals_dates[-90:], max_daily_closes[-90:], label="YTD Closes")
                plt.plot(max_daily_intervals_dates[-90:], twelve_day_EMA[-90:], label="12 EMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], twenty_day_EMA[-90:], label="20 EMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], fifty_day_EMA[-90:], label="50 EMA", linestyle="--")
                plt.plot(max_daily_intervals_dates[-90:], two_hundred_day_EMA[-90:], label="200 EMA", linestyle="--")
                plt.legend()
                plt.show()
            def plotly_plot_EMA():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=max_daily_closes[-90:], name='Closing Price',
                                         line=dict(color='#ef476f', width=4)))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=twenty_day_EMA[-90:], name='20-EMA',
                                          line=dict(color='#f3722c', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=fifty_day_EMA[-90:], name='50-EMA',
                                          line=dict(color='#f9c74f', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=five_day_EMA[-90:], name='5-EMA',
                                          line=dict(color='#90be6d', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=one_hundred_day_EMA[-90:], name='100-EMA',
                                          line=dict(color='#577590', width=4, dash='dot')))
                fig.add_trace(go.Scatter(x=max_daily_intervals_dates[-90:], y=twelve_day_EMA[-90:], name='12-EMA',
                                          line=dict(color='#277da1', width=4, dash='dot')))

                fig.update_layout(title=ticker + ' - EMA Data',
                                  xaxis_title='Date',
                                  yaxis_title='Dollars')

                fig.show()

            # plot_SMA_data()
            # plot_EMA_data()
            plotly_plot_SMA()
            plotly_plot_EMA()
        def calculate_average_volumes(x):
            global last5AverageVolume, last10AverageVolume, last20AverageVolume, last50AverageVolume
            global last100AverageVolume, last200AverageVolume
            last5Volume = max_daily_volumes[-5:]
            last5AverageVolume = sum(last5Volume) / 5
            last10Volume = max_daily_volumes[-10:]
            last10AverageVolume = sum(last10Volume) / 10
            last20Volume = max_daily_volumes[-20:]
            last20AverageVolume = sum(last20Volume) / 20
            last50Volume = max_daily_volumes[-50:]
            last50AverageVolume = sum(last50Volume) / 50
            last100Volume = max_daily_volumes[-100:]
            last100AverageVolume = sum(last100Volume) / 100
            last200Volume = max_daily_volumes[-200:]
            last200AverageVolume = sum(last200Volume) / 200
        def determine_RSI(x):
            # Code for calcualting the RSI of stock
            delta = dataFrame['Adj Close'].diff(1)
            delta.dropna(inplace=True)
            positive = delta.copy()
            negative = delta.copy()
            positive[positive < 0] = 0
            negative[negative > 0] = 0
            days = 14
            averageGain = positive.rolling(window=days).mean()
            averageLoss = abs(negative.rolling(window=days).mean())
            relativeStrength = averageGain / averageLoss
            RSI = 100 - (100 / (1 + relativeStrength))
            global last14RSI
            last14RSI = RSI[-14:]
            print(last14RSI)

            # Code for plotting
            def plotRSI():
                combined = pd.DataFrame()
                combined['Adj Close'] = dataFrame['Adj Close']
                combined['RSI'] = RSI
                plt.figure(figsize=(12, 8))
                # Code for axis 1 for adjusted close value plot
                ax1 = plt.subplot(211)
                ax1.grid(True, color='k', linestyle=':')
                ax1.plot(combined.index[-14:], combined['Adj Close'][-14:], color='lightgray')
                ax1.set_title("Adjusted Close Price Last 14 Days")

                # ax1.grid(True, color='#555555')
                ax1.set_axisbelow(True)
                ax1.set_facecolor('gray')
                # ax1.figure.set_facecolor('#121212')
                ax1.tick_params(axis="x", color="white")
                ax1.tick_params(axis="y", color="white")

                # Code for axis 2 for RSI
                ax2 = plt.subplot(212, sharex=ax1)
                ax2.plot(combined.index[-14:], combined['RSI'][-14:], color='lightgray')
                ax2.axhline(0, linestyle='--', alpha=0.5, color='#ff0000')
                ax2.axhline(10, linestyle='--', alpha=0.5, color='#ffaa00')
                ax2.axhline(20, linestyle='--', alpha=0.5, color='#00ff00')
                ax2.axhline(30, linestyle='--', alpha=0.5, color='#cccccc')
                ax2.axhline(70, linestyle='--', alpha=0.5, color='#cccccc')
                ax2.axhline(80, linestyle='--', alpha=0.5, color='#00ff00')
                ax2.axhline(90, linestyle='--', alpha=0.5, color='#ffaa00')
                ax2.axhline(100, linestyle='--', alpha=0.5, color='#ff0000')

                ax2.set_title("RSI Value Last 14 Days")
                ax2.grid(False)
                ax2.set_axisbelow(True)
                ax2.set_facecolor('gray')
                ax2.tick_params(axis="x", color="white")
                ax2.tick_params(axis="y", color="white")

                plt.show()

            # plotRSI()

            #  RSI trading strategy
            def RSIStrat():
                oversold = 0
                overbought = 0
                normal = 0
                for x in last14RSI:
                    if x <= 30:
                        oversold += 1
                    elif x >= 70:
                        overbought += 1
                    elif x > 30 and x < 70:
                        normal += 1
                print(overbought)
                print(oversold)
                print(normal)
                if (overbought > oversold) & (overbought > normal):
                    print('Asset is overbought, sell signal.')
                elif (oversold > overbought) & (oversold > normal):
                    print('Asset is oversold, buy signal.')
                elif (normal > overbought) & (normal > oversold):
                    print('Asset is in normal range, neutral signal.')

            # RSIStrat()
        def fib_retracement(x):
            dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
            # Grabs max and min of adjusted close data for time frame
            priceMin = dataFrame['Adj Close'].min()
            priceMax = dataFrame['Adj Close'].max()
            # Fib calculations
            diff = priceMax - priceMin
            level1 = priceMax - (.236 * diff)
            level2 = priceMax - (.382 * diff)
            level3 = priceMax - (.618 * diff)
            print("Level", "Price")
            print("0 ", priceMax)
            print(".236", level1)
            print(".382", level2)
            print(".618", level3)
            print("1", priceMin)

            # Graphing the data
            def plotData():
                fig, ax = plt.subplots()
                ax.plot(dataFrame['Adj Close'], color='white')
                ax.axhspan(level1, priceMin, alpha=0.4, color='lightsalmon')
                ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod')
                ax.axhspan(level3, level2, alpha=0.5, color='palegreen')
                ax.axhspan(priceMax, level3, alpha=0.5, color='powderblue')
                ax.set_facecolor('silver')
                plt.show()
            # plotData()

        # Calling funtions
        generateStockData(x)
        calc_moving_averages(x)
        calculate_average_volumes(x)
        determine_RSI(x)
        # fib_retracement(x)

        # Code for GUI
        def run_gui():
            window = Tk()
            window.title('Stock Analysis')
            window.geometry("700x700")

            # Yesterdays close label
            yesterdays_close_lbl = Label(window, text="Yesterdays Close --->" + str(yesterdays_close))
            # Moving averages labels
            five_SMA_lbl = Label(window, text="5-SMA --->" + str(five_day_SMA[-1]))
            ten_SMA_lbl = Label(window, text="10-SMA --->" + str(ten_day_SMA[-1]))
            twenty_SMA_lbl = Label(window, text="20-SMA --->" + str(twenty_day_SMA[-1]))
            fifty_SMA_lbl = Label(window, text="50-SMA --->" + str(fifty_day_SMA[-1]))
            one_hundred_SMA_lbl = Label(window, text="100-SMA --->" + str(one_hundred_day_SMA[-1]))
            two_hundred_SMA_lbl = Label(window, text="200-SMA --->" + str(two_hundred_day_SMA[-1]))
            five_EMA_lbl = Label(window, text="5-EMA --->" + str(five_day_EMA[-1]))
            ten_EMA_lbl = Label(window, text="10-EMA --->" + str(ten_day_EMA[-1]))
            twenty_EMA_lbl = Label(window, text="20-EMA --->" + str(twenty_day_EMA[-1]))
            fifty_EMA_lbl = Label(window, text="50-EMA --->" + str(fifty_day_EMA[-1]))
            one_hundred_EMA_lbl = Label(window, text="100-EMA --->" + str(one_hundred_day_EMA[-1]))
            two_hundred_EMA_lbl = Label(window, text="200-EMA --->" + str(two_hundred_day_EMA[-1]))
            # Stock volumes
            five_day_volume_lbl = Label(window, text="5-Volume ---> " + str(last5AverageVolume))
            ten_day_volume_lbl = Label(window, text="10-Volume ---> " + str(last10AverageVolume))
            twenty_day_volume_lbl = Label(window, text="20-Volume ---> " + str(last20AverageVolume))
            fifty_day_volume_lbl = Label(window, text="50-Volume ---> " + str(last50AverageVolume))
            one_hundred_day_volume_lbl = Label(window, text="100-Volume ---> " + str(last100AverageVolume))
            two_hundred_day_volume_lbl = Label(window, text="200-Volume ---> " + str(last200AverageVolume))

            # Stock information labels
            long_business_summary_lbl = Label(window, text='Business Summary ---> ' + long_business_summary,
                                               wraplength=500, justify='left')
            # Putting yesterdays close on gui
            yesterdays_close_lbl.grid(column=0, row=0, padx=10)
            # Putting the SMAs on gui
            five_SMA_lbl.grid(column=1, row=0, padx=10)
            ten_SMA_lbl.grid(column=1, row=1, padx=10)
            twenty_SMA_lbl.grid(column=1, row=2, padx=10)
            fifty_SMA_lbl.grid(column=1, row=3, padx=10)
            one_hundred_SMA_lbl.grid(column=1, row=4, padx=10)
            two_hundred_SMA_lbl.grid(column=1, row=5, padx=10)
            # Putting the EMAs on gui
            five_EMA_lbl.grid(column=2, row=0, padx=10)
            ten_EMA_lbl.grid(column=2, row=1, padx=10)
            twenty_EMA_lbl.grid(column=2, row=2, padx=10)
            fifty_EMA_lbl.grid(column=2, row=3, padx=10)
            one_hundred_EMA_lbl.grid(column=2, row=4, padx=10)
            two_hundred_EMA_lbl.grid(column=2, row=5, padx=10)
            # Putting volumes on GUI
            five_day_volume_lbl.grid(column=0, row=1)
            ten_day_volume_lbl.grid(column=0, row=2)
            twenty_day_volume_lbl.grid(column=0, row=3)
            fifty_day_volume_lbl.grid(column=0, row=4)
            one_hundred_day_volume_lbl.grid(column=0, row=5)
            two_hundred_day_volume_lbl.grid(column=0, row=6)
            # Putting stock information on gui
            # long_business_summary_lbl.grid(column=1,pady=15)
            # Run tkinter
            window.mainloop()

        run_gui()

    create_tkinter()

    # for col in max_daily_intervals:
    #     print(col)


# Run code
userTicker = input('Enter a ticker for a stock in lowercase to \n generate a data frame'
                   ' and to generate info about the stock: ')
grabDataYahooFinance(userTicker)
