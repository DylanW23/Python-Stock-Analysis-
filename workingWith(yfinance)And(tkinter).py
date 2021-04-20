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



# Function for letting the user grab data from yfinance
def grabDataYahooFinance(x):
    ticker = userTicker.strip().upper()
    yahooFinanceTicker = yf.Ticker(ticker)
    dataFrame = pdr.get_data_yahoo(ticker, start=startDate, end=today)
    closesSince2000 = dataFrame['Adj Close']
    global fiftyDaySMA
    fiftyDaySMA = 0
    global twoHundredDaySMA
    twoHundredDaySMA = 0

    # This prints all the data that can be generated from the dataframe
    for col in dataFrame:
        print(col)

    # Determines the 50 day moving average for the stock the user inputs
    def determineFiftyDayMA(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
        last50Closes = dataFrame['Adj Close'][-50:]
        sumOfLast50 = sum(last50Closes)
        global fiftyDaySMA
        fiftyDaySMA = sumOfLast50 / 50

    # Determine the 200 day moving average for the stock the user inputs
    def determine200DayMA(x):
        dataFrame = pdr.get_data_yahoo(x, start=startDate, end=today)
        last200Closes = dataFrame['Adj Close'][-200:]
        sumOfLast200 = sum(last200Closes)
        global twoHundredDaySMA
        twoHundredDaySMA = sumOfLast200 / 200

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

    def createCandleSticks(x):
        data = pdr.get_data_yahoo(x, start=startDate, end=today)
        print(mpf.available_styles())
        mpf.plot(data, type="candle", style="binance")



    # Calling functions and running code
    determine200DayMA(userTicker)
    determineFiftyDayMA(userTicker)
    determineRSI(userTicker)
    createCandleSticks(userTicker)


    print("50 Day Moving Average ---> " + str(fiftyDaySMA))
    print("200 Day Moving Average ---> " + str(twoHundredDaySMA))





# Tkinter
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


# Run code
userTicker = input('Enter a ticker for a stock in lowercase to \n generate a data frame'
          ' and to generate info about the stock: ')
# generateStockData(userTicker)
grabDataYahooFinance(userTicker)




