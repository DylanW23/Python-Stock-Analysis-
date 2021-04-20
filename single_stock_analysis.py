
# Imports for pandas datareaders and datetime
import pandas_datareader as pdr
import datetime
# Import Matplotlib's `pyplot` module as `plt`
import matplotlib.pyplot as plt
# Import `numpy` as `np`
import numpy as np

# ORGANIZING AND DISPLAYING DATA IN TABLES AND GRAPHS
# Apple stock info starting 1/1/2020 to the current date
aapl = pdr.get_data_yahoo('AAPL',
                          start=datetime.datetime(2004, 12, 31),
                          end=datetime.datetime(2021, 4, 6))
# Variables storing the data pulled in
appleHead = aapl.head()
appleTail = aapl.tail()
appleDescribe = aapl.describe()
# Printing the variables
print('--------------------------------------------------------------')
print('Prints data from the beginning of the time frame given.')
print(appleHead)
print('--------------------------------------------------------------')
print('Prints data from the end of the time frame given.')
print(appleTail)
print('--------------------------------------------------------------')
print('Prints different data about the time frame given.')
print(appleDescribe)
print('--------------------------------------------------------------')
# Resample to monthly level
print('Prints the average highs and lows for the months as well as volume.')
monthly_aapl = aapl.resample('M').mean()
# Print the monthly highs and lows for apple in 2020
print(monthly_aapl)
print('--------------------------------------------------------------')
# Plot the closing prices for `aapl`, shows the plot for apple
aapl['Close'].plot(grid=True)
plt.show()

# USING DATA FOR FINANCIAL ANLYSIS
# Assign `Adj Close` to `daily_close`
daily_close = aapl[['Adj Close']]
# Daily returns
daily_pct_change = daily_close.pct_change()
# Replace NA values with 0
daily_pct_change.fillna(0, inplace=True)
# Inspect daily returns
print(daily_pct_change)
print('--------------------------------------------------------------')
# Daily log returns
daily_log_returns = np.log(daily_close.pct_change()+1)
# Print daily log returns
print(daily_log_returns)
print('--------------------------------------------------------------')

# Resample `aapl` to business months, take last observation as value
print('Monthly percentage change of asset')
monthly = aapl.resample('BM').apply(lambda x: x[-1])
# Calculate the monthly percentage change
print(monthly.pct_change())
print('--------------------------------------------------------------')
print('Quarterly percentage change of asset')
# Resample `aapl` to quarters, take the mean as value per quarter
quarter = aapl.resample("4M").mean()
# Calculate the quarterly percentage change
print(quarter.pct_change())
# Daily returns
print('--------------------------------------------------------------')
print('Prints daily return of stock')
daily_pct_change = daily_close / daily_close.shift(1) - 1
print(daily_pct_change)
print('--------------------------------------------------------------')
print('Cummulative daily return for the intervals listed')
# Calculate the cumulative daily returns
cum_daily_return = (1 + daily_pct_change).cumprod()
print(cum_daily_return)
# Plot the cumulative daily returns
# cum_daily_return.plot(figsize=(12,8))
# plt.show()
# Resample the cumulative daily return to cumulative monthly return
print('--------------------------------------------------------------')
print('Cummulative mothly return for the intervals listed')
cum_monthly_return = cum_daily_return.resample("M").mean()
print(cum_monthly_return)