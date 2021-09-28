from numpy.core.numeric import NaN
import robin_stocks as rh
import pandas_datareader as web
import userFunctions as uf
from pprint import pprint
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt
import numpy as np

# To add:
# charting functions
# Sharpe Ratio
# Beta
# Max Drawdown
# Volatility


class Portfolio():

    def __init__(self):
        date = dt.date.today()
        date = date.strftime("%Y_%m_%d")

        # minimize API calls pulling data once per day
        if os.path.exists(f'portfolio_{date}.csv') and os.path.exists(f'bank_transfers_{date}.csv'):
            self.data = pd.read_csv(f'portfolio_{date}.csv')
            self.bank_transfers = pd.read_csv(f'bank_transfers_{date}.csv')
        else:
            uf.login()
            self.data = pd.DataFrame(rh.get_historical_portfolio(
                interval='week', span='all')['equity_historicals'])
            self.data.to_csv(f'portfolio_{date}.csv')
            self.bank_transfers = pd.DataFrame(rh.get_bank_transfers())
            print(self.bank_transfers)

            for ix in self.bank_transfers.index:
                if self.bank_transfers.at[ix, 'direction'] == 'withdraw':
                    self.bank_transfers.at[ix, 'amount'] = - \
                        float(self.bank_transfers.at[ix, 'amount'])
            self.bank_transfers.to_csv(f'bank_transfers_{date}.csv')

        # Convert Dates to datetime objects
        for ix in self.data.index:
            self.data.at[ix, 'begins_at'] = dt.datetime.strptime(
                self.data.at[ix, 'begins_at'][0:10], "%Y-%m-%d")

        for ix in self.bank_transfers.index:
            self.bank_transfers.at[ix, 'created_at'] = dt.datetime.strptime(
                self.bank_transfers.at[ix, 'created_at'][0:10], "%Y-%m-%d")

        self.data['adjusted_close_equity'] = self.data['adjusted_close_equity'].astype(
            float)
        self.data['adjusted_open_equity'] = self.data['adjusted_open_equity'].astype(
            float)
        self.data['close_equity'] = self.data['close_equity'].astype(float)
        self.data['open_equity'] = self.data['open_equity'].astype(float)

    def get_benchmark_data(self, benchmark_ticker):
        start_date = self.data.at[0, 'begins_at']
        # Get benchmark data from yahoo finance API
        self.benchmark_data = web.DataReader(
            benchmark_ticker, 'yahoo', start_date, dt.date.today())

        print(self.benchmark_data)
        self.benchmark_closes = []
        self.benchmark_opens = []
        self.benchmark_adj_closes = []

        for ix in self.data.index:
            date = self.data.at[ix, 'begins_at']
            try:
                self.benchmark_closes.append(
                    self.benchmark_data.at[date, 'Close'])
                self.benchmark_opens.append(
                    self.benchmark_data.at[date, 'Open'])
                self.benchmark_adj_closes.append(
                    self.benchmark_data.at[date, 'Adj Close'])
            except:
                date = date + dt.timedelta(days=1)
                self.benchmark_closes.append(
                    self.benchmark_data.at[date, 'Close'])
                self.benchmark_opens.append(
                    self.benchmark_data.at[date, 'Open'])
                self.benchmark_adj_closes.append(
                    self.benchmark_data.at[date, 'Adj Close'])

        self.data['benchmark_close'] = self.benchmark_closes
        self.data['benchmark_open'] = self.benchmark_opens
        self.data['benchmark_adj_close'] = self.benchmark_adj_closes
        return self.benchmark_data

    def get_benchmark_weekly_returns(self):
        # CLose to Close
        self.benchmark_weekly_pct_returns = []
        for ix in self.data.index:
            if ix == 0:
                self.benchmark_weekly_pct_returns.append(
                    (self.data.at[ix+1, 'benchmark_adj_close'] - self.data.at[ix, 'benchmark_adj_close'])/self.data.at[ix, 'benchmark_close'])
            elif ix == self.data.index[-1]:
                self.benchmark_weekly_pct_returns.append(NaN)
            else:
                self.benchmark_weekly_pct_returns.append(
                    (self.data.at[ix+1, 'benchmark_adj_close'] - self.data.at[ix, 'benchmark_adj_close'])/self.data.at[ix, 'benchmark_close'])
        self.data['benchmark_weekly_returns'] = self.benchmark_weekly_pct_returns
        return self.benchmark_weekly_pct_returns

    def get_weekly_returns(self):
        # CLose to Close
        self.weekly_pct_returns = []
        for ix in self.data.index:
            if ix == 0:
                self.weekly_pct_returns.append(
                    (self.data.at[ix+1, 'adjusted_close_equity'] - self.data.at[ix, 'adjusted_close_equity'])/self.data.at[ix, 'close_equity'])
            elif ix == self.data.index[-1]:
                self.weekly_pct_returns.append(NaN)
            else:
                self.weekly_pct_returns.append(
                    (self.data.at[ix+1, 'adjusted_close_equity'] - self.data.at[ix, 'adjusted_close_equity'])/self.data.at[ix, 'close_equity'])
        self.data['weekly_returns'] = self.weekly_pct_returns
        return self.weekly_pct_returns

    def get_anualized_volatility(self, period='week'):
        # add start end date functionality
        if period == 'week':
            self.annual_volatility = np.std(
                self.weekly_pct_returns[:-1]) * (52**0.5)
        return self.annual_volatility

    def get_benchmark_annualized_volatility(self, period='week'):
        # add start end date functionality
        if period == 'week':
            self.benchmark_annual_volatility = np.std(
                self.benchmark_weekly_pct_returns[:-1]) * (52**0.5)
        return self.benchmark_annual_volatility

    def get_beta(self, start_date, end_date):
        data = self.data.dropna()
        data.where((data['begins_at'] > start_date) & (
            data['begins_at'] < end_date), inplace=True)
        data.dropna(inplace=True)
        data = data.filter(
            items=['weekly_returns', 'benchmark_weekly_returns'])
        self.cov = pd.DataFrame.cov(data)
        print(self.cov)
        self.beta = self.cov.at['weekly_returns', 'benchmark_weekly_returns'] / \
            self.cov.at['weekly_returns', 'weekly_returns']
        print(self.beta)

    def get_sharp_ratio(self, start_date, end_date, rfr=0.01):
        data = self.data.dropna()
        data.where((data['begins_at'] > start_date) & (
            data['begins_at'] < end_date), inplace=True)
        data.dropna(inplace=True)
        std = np.std(data['weekly_returns']) * (52**0.5)
        ave_returns = np.average(data['weekly_returns'])
        ave_returns_annualized = ave_returns*52
        self.sharpe = (ave_returns_annualized - rfr) / std
        print(self.sharpe)
        return self.sharpe

        # print(self.bank_transfers['created_at'])

        # self.dates = []
        # self.total_deposits = []
        # self.close_equity = []
        # self.returns = []
        # self.pct_returns = []
        # for ix in self.data.index:
        #     date = dt.datetime.strptime(self.data.at[ix, 'begins_at'][0:10], "%Y-%m-%d" )
        #     self.dates.append(date)
        #     deposit = self.bank_transfers[(self.bank_transfers['created_at'] < date)]['amount'].sum()
        #     self.total_deposits.append(deposit)
        #     self.close_equity.append(self.data.at[ix, 'close_equity'])
        #     self.returns.append(self.data.at[ix, 'close_equity'] - deposit)
        #     self.pct_returns.append((self.data.at[ix, 'close_equity'] - deposit) / deposit)
        # self.weekly_returns = [self.returns[i+1] -self.returns[i] for i in range(len(self.dates)-1)]
        # self.weekly_pct_returns = [self.pct_returns[i+1] -self.pct_returns[i] for i in range(len(self.dates)-1)]
        # self.weekly_returns.insert(0, 0)
        # self.weekly_pct_returns.insert(0, 0)

        # print(self.dates)
        # print(self.total_deposits)
        # print(self.close_equity)
        # print(self.returns)
        # print(self.pct_returns)
        # print(self.weekly_returns)
        # print(self.weekly_pct_returns)
        # plt.plot(self.total_deposits)
        # plt.show()

        # pprint(self.bank_transfers)

        # plt.plot(self.data['close_equity'])
        # plt.show()

        # uf.login()
        # bank_transfers = rh.get_bank_transfers()
        # pprint(bank_transfers)
        # bank_transfers = pd.DataFrame(bank_transfers)
        # pprint(bank_transfers)


if __name__ == '__main__':
    # uf.login()
    # hist = rh.get_historical_portfolio(interval='week', span='all')
    # print(hist)
    # df = pd.DataFrame(hist['equity_historicals'])
    # pprint(df)
    portfolio = Portfolio()
    portfolio.get_benchmark_data('TSLA')
    portfolio.get_weekly_returns()
    vol = portfolio.get_anualized_volatility()
    portfolio.get_benchmark_weekly_returns()
    bv = portfolio.get_benchmark_annualized_volatility()
    print(bv)
    print(vol)
    start = dt.datetime(2020, 1, 17)
    end = dt.datetime(2021, 9, 15)
    portfolio.get_beta(start, end)
    portfolio.get_sharp_ratio(start, end)