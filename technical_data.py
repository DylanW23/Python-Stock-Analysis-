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

# yf.pdr_override()
today = date.today()
startDate = "2020-01-01"



# Function to generate stock data using yfinance
def generateStockData(x):
    ticker = x.strip().upper()
    yfTicker = yf.Ticker(ticker)
    Info = yfTicker.info
    Dividends = yfTicker.dividends
    Actions = yfTicker.actions
    Splits = yfTicker.splits
    Financials = yfTicker.financials
    majorHolders = yfTicker.major_holders
    instituionalHolders = yfTicker.institutional_holders
    Recomendations = yfTicker.recommendations
    print("---------------------------------------------------")
    print("Here is a summary information about " + ticker + ".")
    print(Info['longBusinessSummary'])
    print("---------------------------------------------------")

# Function for letting the user grab data from yfinance
def grabDataYahooFinance(x):
    # User input and passing it to yfinance
    ticker = userTicker.strip().upper()
    data = yf.Ticker(x)
    yahooFinanceTicker = yf.Ticker(ticker)
    dataFrame = pdr.get_data_yahoo(ticker, start=startDate, end=today)

    # Daily closes for the total lifetime of a stock
    max_daily_intervals = data.history(period='max', interval='1d')
    # A list of all the daily closes for total lifetime of stock
    max_daily_closes = (max_daily_intervals['Close'])
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
    # This prints all the data that can be generated from the dataframe



    def simple_moving_averages(x):
        # Creates SMA based off ytd data
        global five_day_SMA, ten_day_SMA, twenty_day_SMA,fifty_day_SMA,one_hundred_day_SMA,two_hundred_day_SMA,ytd_SMA
        five_day_SMA = max_daily_closes.rolling(5, min_periods=1).mean()
        ten_day_SMA = max_daily_closes.rolling(10, min_periods=1).mean()
        twenty_day_SMA = max_daily_closes.rolling(20, min_periods=1).mean()
        fifty_day_SMA = max_daily_closes.rolling(50, min_periods=1).mean()
        one_hundred_day_SMA = max_daily_closes.rolling(100, min_periods=1).mean()
        two_hundred_day_SMA = max_daily_closes.rolling(200, min_periods=1).mean()
        ytd_SMA = ytd_daily_closes.rolling(365, min_periods=1).mean()
        print("5-Day SMA " + str(five_day_SMA[-1]))
        print("10-Day SMA " + str(ten_day_SMA[-1]))
        print("20-Day SMA " + str(twenty_day_SMA[-1]))
        print("50-Day SMA " + str(fifty_day_SMA[-1]))
        print("100-Day SMA " + str(one_hundred_day_SMA[-1]))
        print("200-Day SMA " + str(two_hundred_day_SMA[-1]))
        print("YTD-SMA " + str(ytd_SMA[-1]))
        def plot_data():
            rcParams['figure.figsize'] = 12,6
            plt.grid(True, color='k', linestyle=":")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.title(ticker + " Moving Averages, 2 Year Time Frame")
            plt.plot(max_daily_intervals_dates[-730:],max_daily_closes[-730:], label = "YTD Closes")
            # plt.plot(ytd_intervals_dates, ytd_SMA, label="YTD SMA", linestyle="--")
            plt.plot(max_daily_intervals_dates[-730:], twenty_day_SMA[-730:], label="20 SMA", linestyle="--")
            plt.plot(max_daily_intervals_dates[-730:], fifty_day_SMA[-730:], label="50 SMA", linestyle="--")
            plt.plot(max_daily_intervals_dates[-730:], two_hundred_day_SMA[-730:], label="200 SMA", linestyle="--")

            plt.legend()
            plt.show()

        plot_data()

    def estimated_moving_averages(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
        ten_day_ema = pd.Series.ewm(max_daily_closes, span=10).mean()
        eight_day_ema = pd.Series.ewm(max_daily_closes, span=8).mean()
        twelve_day_ema =  pd.Series.ewm(max_daily_closes, span=12).mean()
        twenty_day_ema = pd.Series.ewm(max_daily_closes, span=20).mean()
        twenty_six_day_ema = pd.Series.ewm(max_daily_closes, span=26).mean()
        fifty_day_ema = pd.Series.ewm(max_daily_closes, span=50).mean()
        two_hundred_day_ema = pd.Series.ewm(max_daily_closes, span=200).mean()
        print("10 EMA - " + str(ten_day_ema[-1]))
        print("8 EMA - " + str(eight_day_ema[-1]))
        print("12 EMA - " + str(twelve_day_ema[-1]))
        print("20 EMA - " + str(twenty_day_ema[-1]))
        print("50 EMA - " + str(fifty_day_ema[-1]))
        print("200 EMA - " + str(two_hundred_day_ema[-1]))
        MACD = twelve_day_ema - twenty_six_day_ema


    def calculateAverageVolumes(x):
        last5Volume = max_daily_volumes[-5:]
        last5AverageVolume = sum(last5Volume)/5
        last10Volume = max_daily_volumes[-10:]
        last10AverageVolume = sum(last10Volume)/10
        last20Volume = max_daily_volumes[-20:]
        last20AverageVolume = sum(last20Volume)/20
        last50Volume = max_daily_volumes[-50:]
        last50AverageVolume = sum(last50Volume)/50
        last100Volume = max_daily_volumes[-100:]
        last100AverageVolume = sum(last100Volume)/100
        last200Volume = max_daily_volumes[-200:]
        last200AverageVolume = sum(last200Volume)/200
        print("5-Day Volume "+str(last5AverageVolume))
        print("10-Day Volume "+str(last10AverageVolume))
        print("20-Day Volume "+str(last20AverageVolume))
        print("50-Day Volume "+str(last50AverageVolume))
        print("100-Day Volume "+str(last100AverageVolume))
        print("200-Day Volume "+str(last200AverageVolume))

    # Function to determine RSI, <30 is considered oversold >70 is considered overbought
    # Add functions to determine if overbought and oversold and have the
    # Program predict wether it is giving a sell or buy signal based on the
    # RSI
    def determineRSI(x):
        # Code for calcualting the RSI of stock
        delta = dataFrame['Adj Close'].diff(1)
        delta.dropna(inplace=True)
        positive = delta.copy()
        negative = delta.copy()
        positive[positive<0] = 0
        negative[negative>0] = 0
        days = 14
        averageGain = positive.rolling(window=days).mean()
        averageLoss = abs(negative.rolling(window=days).mean())
        relativeStrength = averageGain/averageLoss
        RSI = 100 - (100/(1+relativeStrength))
        print(RSI)
        global last14RSI
        last14RSI = RSI[-14:]
        print(last14RSI)
        # Code for plotting
        def plotRSI():
            combined = pd.DataFrame()
            combined['Adj Close'] = dataFrame['Adj Close']
            combined['RSI'] = RSI
            plt.figure(figsize=(12,8))
            # Code for axis 1 for adjusted close value plot
            ax1 = plt.subplot(211)
            ax1.plot(combined.index, combined['Adj Close'], color='lightgray')
            ax1.set_title("Adjusted Close Price", color='white')

            ax1.grid(True, color='#555555')
            ax1.set_axisbelow(True)
            ax1.set_facecolor('black')
            ax1.figure.set_facecolor('#121212')
            ax1.tick_params(axis="x", color="white")
            ax1.tick_params(axis="y", color="white")

            # Code for axis 2 for RSI
            ax2 =plt.subplot(212, sharex=ax1)
            ax2.plot(combined.index, combined['RSI'], color='lightgray')
            ax2.axhline(0, linestyle='--', alpha=0.5, color='#ff0000')
            ax2.axhline(10, linestyle='--', alpha=0.5, color='#ffaa00')
            ax2.axhline(20, linestyle='--', alpha=0.5, color='#00ff00')
            ax2.axhline(30, linestyle='--', alpha=0.5, color='#cccccc')
            ax2.axhline(70, linestyle='--', alpha=0.5, color='#cccccc')
            ax2.axhline(80, linestyle='--', alpha=0.5, color='#00ff00')
            ax2.axhline(90, linestyle='--', alpha=0.5, color='#ffaa00')
            ax2.axhline(100, linestyle='--', alpha=0.5, color='#ff0000')

            ax2.set_title("RSI Value")
            ax2.grid(False)
            ax2.set_axisbelow(True)
            ax2.set_facecolor('black')
            ax2.tick_params(axis="x", color="white")
            ax2.tick_params(axis="y", color="white")

            plt.show()
        plotRSI()
        #  RSI trading strategy
        def RSIStrat():
            oversold = 0
            overbought = 0
            normal = 0
            for x in last14RSI:
                if x<=30:
                    print("The rsi at this point is less than 30, which means oversold")
                    oversold += 1
                elif x>=70:
                    print("The rsi at this point is greater than 70 which means overbought")
                    overbought += 1
                elif x>30 and x<70:
                    print("This is in the middle which means normal action. ")
                    normal += 1
            print(overbought)
            print(oversold)
            print(normal)



    # Creates candlesticks for the stock / etf
    # Add functionality to click on candlesticks to see the highs, lows, opens and closes
    def createCandleSticks(x):
        data = pdr.get_data_yahoo(start=startDate,end=today)
        colors = mpf.make_marketcolors(up="#00ff00",
                                       down="#ff0000",
                                       wick="inherit",
                                       edge="inherit",
                                       volume="in")
        mpfStyle = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=colors)
        mpf.plot(data, type="candle", style=mpfStyle, volume=True)

    # IMPORTANT TO NOTE
    # This will show fib retracement levels for the dates inputted
    # They could change based on time frame
    # Need to add functionality to be able to show multiple time frames
    def fibRetracement(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
        # Grabs max and min of adjusted close data for time frame
        priceMin = dataFrame['Adj Close'].min()
        priceMax = dataFrame['Adj Close'].max()
        # Fib calculations
        diff = priceMax-priceMin
        level1 = priceMax - (.236*diff)
        level2 = priceMax - (.382*diff)
        level3 = priceMax - (.618*diff)
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

    # Tkinter
    # Add functionality to display all the information above on gui
    def runTkinter():
        window = Tk()
        window.title('Plotting in Tkinter')
        window.geometry("500x500")
        plot_button = Button(master=window,
                             height=2,
                             width=10,
                             text="Plot")
        plot_button.pack()
        window.mainloop()


    print("Yesterday's adjusted close was -----> " + str(yesterdays_close))
    # createCandleSticks(userTicker)
    # determineRSI(userTicker)
    # calculateAverageVolumes(userTicker)
    # fibRetracement(userTicker)
    simple_moving_averages(userTicker)
    estimated_moving_averages(userTicker)
    for col in max_daily_intervals:
        print(col)


# Run code
userTicker = input('Enter a ticker for a stock in lowercase to \n generate a data frame'
          ' and to generate info about the stock: ')
# generateStockData(userTicker)
generateStockData(userTicker)
grabDataYahooFinance(userTicker)
