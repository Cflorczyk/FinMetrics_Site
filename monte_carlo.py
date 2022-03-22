import pandas as pd
import datetime as dt
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import style
from matplotlib.ticker import PercentFormatter
import statistics
import yfinance as yf


style.use('seaborn-colorblind')

ticker_id = 'AAPL'
benchmark_id = 'SPY'

years = 1 # make this a user input maybe?
end_date = date.today()
start_date = date.today() - pd.DateOffset(years=years)

ticker_data = yf.download(ticker_id, start_date, end_date)['Adj Close']
benchmark_data = yf.download(benchmark_id, start_date, end_date)['Adj Close']

ticker_returns = ticker_data.pct_change()
benchmark_returns = benchmark_data.pct_change()

ticker_return_cumulative = (ticker_returns + 1).cumprod()
benchmark_return_cumulative = (benchmark_returns + 1).cumprod()


last_price = ticker_data[-1]

# Plot things...
fig = plt.figure()

plt.plot(ticker_return_cumulative)
plt.plot(benchmark_return_cumulative)
fig.autofmt_xdate()
plt.show()


# Number of Simulations
num_simulations = 1000
num_days = 252

simulation_df = pd.DataFrame()

for x in range(num_simulations):
    count = 0
    daily_vol = ticker_returns.std()

    price_series = []

    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)

    for y in range(num_days):
        if count == 251:
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1

    simulation_df[x] = price_series

fig = plt.figure()
fig.suptitle(f'Monte Carlo Simulation: {ticker_id}')
plt.plot(simulation_df)
plt.axhline(y=last_price, color='black', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()


plt.xlabel('Value')
plt.ylabel('Number of simulation in each bin')
plt.title(f'Normal Distribution: {ticker_id}')

x = simulation_df.iloc[-1]

s = x
p = s.plot(kind='hist', bins=30, density=True, facecolor='g', alpha=0.75)

bar_value_to_label = statistics.median(x)
min_distance = float("inf")  # initialize min_distance with infinity
index_of_bar_to_label = 0
for i, rectangle in enumerate(p.patches):  # iterate over every bar
    tmp = abs(  # tmp = distance from middle of the bar to bar_value_to_label
        (rectangle.get_x() +
            (rectangle.get_width() * (1 / 2))) - bar_value_to_label)
    if tmp < min_distance:  # we are searching for the bar with x cordinate
                            # closest to bar_value_to_label
        min_distance = tmp
        index_of_bar_to_label = i
p.patches[index_of_bar_to_label].set_color('grey')
#The colored bar is the Median
plt.show()