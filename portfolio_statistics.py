from numpy.core.numeric import NaN
import pandas_datareader as web
import userFunctions as uf
from pprint import pprint
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt
import numpy as np
import robin_stocks as rh

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

        uf.login()
        # minimize API calls pulling data once per day
        if os.path.exists(f'portfolio_{date}.csv') and os.path.exists(f'bank_transfers_{date}.csv'):
            self.data = pd.read_csv(f'portfolio_{date}.csv')
            self.bank_transfers = pd.read_csv(f'bank_transfers_{date}.csv')
        else:
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

        self.current_acc_value = float(rh.robinhood.load_portfolio_profile()[
            'equity'])

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

    def get_benchmark_sharpe(self, start_date, end_date, rfr=0.01):
        data = self.data.dropna()
        data.where((data['begins_at'] > start_date) & (
            data['begins_at'] < end_date), inplace=True)
        data.dropna(inplace=True)
        std = np.std(data['benchmark_weekly_returns']) * (52**0.5)
        ave_returns = np.average(data['benchmark_weekly_returns'])
        ave_returns_annualized = ave_returns*52
        self.sharpe = (ave_returns_annualized - rfr) / std
        print(self.sharpe)
        return self.sharpe

    def get_average_deposited_cash(self, start=None, end=None):

        ix = self.bank_transfers.index[-1]
        oldest_deposit_date = self.bank_transfers.at[ix, 'created_at']

        if start == None or start < oldest_deposit_date:
            start = oldest_deposit_date

        if end == None:
            end = dt.datetime.today()

        total_days = (end - start).days
        ave_acc_val = 0
        for ix in self.bank_transfers.index:
            if self.bank_transfers.at[ix, 'created_at'] < start:
                ave_acc_val += float(
                    self.bank_transfers.at[ix, 'amount'])*total_days

            elif self.bank_transfers.at[ix, 'created_at'] > start and self.bank_transfers.at[ix, 'created_at'] < end:
                time_effect = (
                    end - self.bank_transfers.at[ix, 'created_at']).days
                ave_acc_val += float(
                    self.bank_transfers.at[ix, 'amount']) * time_effect

        ave_acc_val = ave_acc_val / total_days
        return ave_acc_val

    def get_money_weighted_returns(self, start=None, end=None):
        ave_cash = self.get_average_deposited_cash(start, end)

        if start == None:
            start = self.data.at[0, 'begins_at']

        if end == None:
            end = dt.datetime.now()

        data = self.data.where(self.data['begins_at'] > start)
        data = data.where(self.data['begins_at'] < end)
        data.dropna(inplace=True)

        if end > data.at[data.index[-1], 'begins_at']:
            final_adj_close = self.current_acc_value
        else:
            final_adj_close = float(
                data.at[data.index[-1], 'adjusted_close_equity'])

        begining_adj_close = float(
            data.at[data.index[0], 'adjusted_close_equity'])
        net_change = final_adj_close - begining_adj_close
        money_weighted_pct_return = (net_change / ave_cash) * 100
        return money_weighted_pct_return


if __name__ == '__main__':
    portfolio = Portfolio()
    start = dt.datetime(2020, 6, 19)
    ave_cash = portfolio.get_average_deposited_cash(start=start)
    print(ave_cash)
    money_weighted_return = portfolio.get_money_weighted_returns(start)
    print(money_weighted_return)

    # portfolio.get_benchmark_data('BTC-USD')
    # portfolio.get_weekly_returns()
    # vol = portfolio.get_anualized_volatility()
    # portfolio.get_benchmark_weekly_returns()
    # bv = portfolio.get_benchmark_annualized_volatility()
    # print(bv)
    # print(vol)
    # start = dt.datetime(2020, 1, 17)
    # end = dt.datetime(2021, 9, 15)
    # portfolio.get_beta(start, end)
    # portfolio.get_sharp_ratio(start, end)
    # portfolio.get_benchmark_sharpe(start, end)
