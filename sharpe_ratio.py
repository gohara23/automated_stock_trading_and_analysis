
from numpy.lib.function_base import average
import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def sharpe_ratio(rx, rf, std):
    # rx - expected return
    # rf - risk free rate
    # std - volatility
    sharpe_ratio = (rx-rf)/std
    return sharpe_ratio


def volatility_averageReturn(ticker, years_back):

    # Prepares Ticker Data for Sharpe Ratio Calc

    end_date = dt.date.today()
    current_year = end_date.year
    start_date = end_date - dt.timedelta((years_back+1)*365)


    data = pd.DataFrame(web.DataReader(ticker, 'yahoo', start_date, end_date))

    interval_starts = [dt.date(current_year-i, 1, 1) for i in range(years_back, 0, -1)]
    interval_ends = [dt.date(current_year-i, 12, 31) for i in range(years_back, 0, -1)]
    start_prices = np.zeros(len(interval_starts))
    end_prices = np.zeros(len(interval_ends))
    i = 0
    for date in interval_starts:
        while start_prices[i] == 0:
            try:
                start_prices[i] = data.at[str(interval_starts[i]), 'Adj Close']
            except:
                interval_starts[i] = interval_starts[i] + dt.timedelta(days=1)

        i += 1

    i = 0
    for date in interval_ends:
        while end_prices[i] == 0:
            try:
                end_prices[i] = data.at[str(interval_ends[i]), 'Adj Close']
            except:
                interval_ends[i] = interval_ends[i] - dt.timedelta(days=1)

        i += 1

    returns = [(end_prices[i]-start_prices[i])/start_prices[i] for i in range(0, len(start_prices))]

    volatility = np.std(returns)
    average_return = np.mean(returns)
    return volatility, average_return



if __name__ =='__main__':

    ticker = 'MSFT'
    years_back = 6

    volatility, average_returns = volatility_averageReturn(ticker, years_back)

    sharpe = sharpe_ratio(average_returns, 0.03, volatility)

    print(sharpe)


