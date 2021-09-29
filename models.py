import numpy as np
from scipy.optimize import curve_fit
import pandas_datareader as web
import pandas as pd
import datetime as dt
from pprint import pprint
import matplotlib.pyplot as plt


class Models:
    def __init__(self):
        self.ticker_data = {}
        self.ticker_dfs = {}

    @staticmethod
    def first_order_two_variable(X, a, b, c):
        print(X, a, b, c)
        x, y = X
        return a*x + b*y + c

    def add_ticker(self, ticker, start_date):
        df = web.DataReader(ticker, 'yahoo', start_date, dt.date.today())
        dates = [pd.Timestamp.to_pydatetime(date) for date in df.index]
        closes = [close for close in df['Close']]
        adj_closes = [adj_close for adj_close in df['Adj Close']]
        opens = [open for open in df['Open']]
        daily_returns = []
        for ix in range(1, len(opens)):
            daily_returns.append((closes[ix]-closes[ix-1])/closes[ix-1])

        self.ticker_data[ticker] = {
            "Date": dates[1:],
            "Close": closes[1:],
            "Adj_Close": adj_closes[1:],
            "Open": opens[1:],
            "daily_return": daily_returns
        }
        self.ticker_dfs[ticker] = pd.DataFrame(self.ticker_data[ticker])
        self.ticker_dfs[ticker].set_index("Date", inplace=True)

    def add_crypto_match_dates(self, ticker, dates, other_ticker):
        # necessary to align dates with equities
        # also may be used to match other dates
        df = web.DataReader(ticker, 'yahoo', dates[0], dt.date.today())
        df_other = self.ticker_dfs[other_ticker]
        df.index = [pd.Timestamp.to_pydatetime(date) for date in df.index]
        df = df[df.index.isin(dates)]
        dates = [pd.Timestamp.to_pydatetime(date) for date in df.index]
        df_other = df_other[df_other.index.isin(dates)]

        self.ticker_dfs[other_ticker] = df_other.iloc[1:]

        closes = [close for close in df['Close']]
        adj_closes = [adj_close for adj_close in df['Adj Close']]
        opens = [open for open in df['Open']]
        daily_returns = []
        for ix in range(1, len(opens)):
            daily_returns.append((closes[ix]-closes[ix-1])/closes[ix-1])

        self.ticker_data[ticker] = {
            "Date": dates[1:],
            "Close": closes[1:],
            "Adj_Close": adj_closes[1:],
            "Open": opens[1:],
            "daily_return": daily_returns
        }
        self.ticker_dfs[ticker] = pd.DataFrame(self.ticker_data[ticker])
        self.ticker_dfs[ticker].set_index('Date', inplace=True)

        self.update_ticker_from_df(other_ticker, df_other.iloc[1:])
        print(self.ticker_dfs[ticker])
        print(self.ticker_dfs[other_ticker])

    def update_ticker_from_df(self, ticker, df):
        dates = [pd.Timestamp.to_pydatetime(date) for date in df.index]
        closes = [close for close in df['Close']]
        adj_closes = [adj_close for adj_close in df['Adj_Close']]
        opens = [open for open in df['Open']]
        daily_returns = [ret for ret in df['daily_return']]
        self.ticker_data[ticker] = {
            "Date": dates,
            "Close": closes,
            "Adj_Close": adj_closes,
            "Open": opens,
            "daily_return": daily_returns
        }


    @staticmethod
    def fit():
        pass


if __name__ == "__main__":

    start = dt.datetime(2020, 9, 20)
    mara = 'MARA'
    model = Models()
    model.add_ticker(mara, start)
    btc = 'BTC-USD'
    model.add_crypto_match_dates(btc, model.ticker_data[mara]["Date"], mara)
    jmia = 'JMIA'
    model.add_crypto_match_dates(jmia, model.ticker_data[mara]["Date"], mara)

    p0 = 0.3, 0.8, .02
    popt, pcov = curve_fit(Models.first_order_two_variable, (model.ticker_data[btc]['daily_return'][1:],
                                                             model.ticker_data[jmia]['daily_return']), model.ticker_data[mara]['daily_return'], p0)
    print(popt)
    print(pcov)

    data = [Models.first_order_two_variable((model.ticker_data[jmia]['daily_return'][i], model.ticker_data[jmia]['daily_return'][i]), *popt) for i in range(len(model.ticker_data[jmia]['daily_return']))]
    # plt.plot(Models.first_order_two_variable(
    #     *(model.ticker_data[jmia]['daily_return'], model.ticker_data[jmia]['daily_return']), *popt), '--r')
    plt.plot(data, '--r')
    plt.plot(model.ticker_data[mara]['daily_return'], '-k')
    plt.show()
