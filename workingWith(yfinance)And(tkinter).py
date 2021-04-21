import pandas_datareader as pdr
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
import yfinance as yf
import mplfinance as mpf

yf.pdr_override()
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
    ticker = userTicker.strip().upper()
    yahooFinanceTicker = yf.Ticker(ticker)
    dataFrame = pdr.get_data_yahoo(ticker, start=startDate, end=today)
    closesSince2000 = dataFrame['Adj Close']
    yesterdaysClose = round(dataFrame['Adj Close'][-1],2)
    global twentyDaySMA
    twentyDaySMA = round(0,2)
    global fiftyDaySMA
    fiftyDaySMA = round(0,2)
    global twoHundredDaySMA
    twoHundredDaySMA = round(0,2)
    global last5AverageVolume
    last5AverageVolume = round(0,2)
    global last10AverageVolume
    last10AverageVolume = round(0,2)
    global last20AverageVolume
    last20AverageVolume = round(0,2)
    global last50AverageVolume
    last50AverageVolume = round(0,2)
    global last100AverageVolume
    last100AverageVolume = round(0,2)
    global last200AverageVolume
    last200AverageVolume = round(0,2)
    global yearToDateVolume
    yearToDateVolume = round(0,2)

    # This prints all the data that can be generated from the dataframe
    for col in dataFrame:
        print(col)

    # Determines the 50 day moving average for the stock the user inputs
    def determineMovingAverages(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
        last50Closes = dataFrame['Adj Close'][-50:]
        sumOfLast50 = sum(last50Closes)
        global fiftyDaySMA
        fiftyDaySMA = round(sumOfLast50 / 50,2)

        last200Closes = dataFrame['Adj Close'][-200:]
        sumOfLast200 = sum(last200Closes)
        global twoHundredDaySMA
        twoHundredDaySMA = round(sumOfLast200 / 200,2)

        last20Closes = dataFrame['Adj Close'][-20:]
        sumOfLast20 = sum(last20Closes)
        global twentyDaySMA
        twentyDaySMA = round(sumOfLast20/20,2)


    def calculateAverageVolumes(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)

        last5Volume = dataFrame['Volume'][-5:]
        global last5AverageVolume
        last5AverageVolume = sum(last5Volume)/5

        last10Volume = dataFrame['Volume'][-10:]
        global last10AverageVolume
        last10AverageVolume = sum(last10Volume)/10

        last20Volume = dataFrame['Volume'][-20:]
        global last20AverageVolume
        last20AverageVolume = sum(last20Volume)/20

        last50Volume = dataFrame['Volume'][-50:]
        global last50AverageVolume
        last50AverageVolume = sum(last50Volume)/50

        last100Volume = dataFrame['Volume'][-100:]
        global last100AverageVolume
        last100AverageVolume = sum(last100Volume)/100

        last200Volume = dataFrame['Volume'][-200:]
        global last200AverageVolume
        last200AverageVolume = sum(last200Volume)/200

        lastYearVolume = dataFrame['Volume'][-365:]
        global yearToDateVolume
        yearToDateVolume = sum(lastYearVolume)/365

    # Function to determine RSI, <30 is considered oversold >70 is considered overbought
    # Add functions to determine if overbought and oversold and have the
    # Program predict wether it is giving a sell or buy signal based on the
    # RSI
    def determineRSI(x):
        # Code for calcualting the RSI of stock
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
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

    # Creates candlesticks for the stock / etf
    # Add functionality to click on candlesticks to see the highs, lows, opens and closes
    def createCandleSticks(x):
        data = pdr.get_data_yahoo(x, start=startDate, end=today)
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
        fig, ax = plt.subplots()
        ax.plot(dataFrame['Adj Close'], color='white')
        ax.axhspan(level1, priceMin, alpha=0.4, color='lightsalmon')
        ax.axhspan(level2, level1, alpha=0.5, color='palegoldenrod')
        ax.axhspan(level3, level2, alpha=0.5, color='palegreen')
        ax.axhspan(priceMax, level3, alpha=0.5, color='powderblue')
        plt.ylabel("Price")
        plt.xlabel("Date")
        plt.legend(loc=2)
        ax.set_facecolor('silver')
        plt.show()

    # Tkinter
    # Add functionality to display all the information above on gui
    def runTikinter():
        window = Tk()
        window.title('Plotting in Tkinter')
        window.geometry("500x500")
        plot_button = Button(master=window,
                             height=2,
                             width=10,
                             text="Plot")
        plot_button.pack()
        window.mainloop()

    # Calling functions and running code
    createCandleSticks(userTicker)
    determineRSI(userTicker)
    determineMovingAverages(userTicker)
    calculateAverageVolumes(userTicker)
    fibRetracement(userTicker)

    print("Yesterday's adjusted close was -----> " + str(yesterdaysClose))
    print("20 Day Moving Average -----> " + str(twentyDaySMA))
    print("50 Day Moving Average ---> " + str(fiftyDaySMA))
    print("200 Day Moving Average ---> " + str(twoHundredDaySMA))
    print("Last 20 Days Average Volume -----> " + str(last20AverageVolume))
    print("Last 50 Days Average Volume -----> " + str(last50AverageVolume))
    print("Last 200 Days Average Volume -----> " + str(last200AverageVolume))

# Run code
userTicker = input('Enter a ticker for a stock in lowercase to \n generate a data frame'
          ' and to generate info about the stock: ')
# generateStockData(userTicker)
generateStockData(userTicker)
grabDataYahooFinance(userTicker)




