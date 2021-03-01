
from numpy.lib.function_base import average
import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import rc


class Ticker:
    def __init__(self, ticker, years_back):
        self.ticker = ticker
        end_date = dt.date.today()
        start_date = end_date - dt.timedelta((years_back+1)*365)
        self.data = pd.DataFrame(web.DataReader(self.ticker, 'yahoo', start_date, end_date))
  
        self.volatility, self.average_return, self.returns = self.volatility_averageReturn(years_back, self.data)

    def volatility_averageReturn(self, years_back, ticker_data):

        # Prepares Ticker Data for Sharpe Ratio Calc

        end_date = dt.date.today()
        current_year = end_date.year
        start_date = end_date - dt.timedelta((years_back+1)*365)

        # data = pd.DataFrame(web.DataReader(ticker, 'yahoo', start_date, end_date))

        interval_starts = [dt.date(current_year-i, 1, 1)
                        for i in range(years_back, 0, -1)]
        interval_ends = [dt.date(current_year-i, 12, 31)
                        for i in range(years_back, 0, -1)]
        start_prices = np.zeros(len(interval_starts))
        end_prices = np.zeros(len(interval_ends))
        i = 0
        for date in interval_starts:
            while start_prices[i] == 0:
                try:
                    start_prices[i] = ticker_data.at[str(interval_starts[i]), 'Adj Close']
                except:
                    interval_starts[i] = interval_starts[i] + dt.timedelta(days=1)

            i += 1

        i = 0
        for date in interval_ends:
            while end_prices[i] == 0:
                try:
                    end_prices[i] = ticker_data.at[str(interval_ends[i]), 'Adj Close']
                except:
                    interval_ends[i] = interval_ends[i] - dt.timedelta(days=1)

            i += 1

        returns = [(end_prices[i]-start_prices[i])/start_prices[i]
                for i in range(0, len(start_prices))]

        volatility = np.std(returns)
        average_return = np.mean(returns)
        return volatility, average_return, returns


class Portfolio:
    def __init__(self, tickers, weights, years_back):
        # self.tickers = [Ticker(ticker, years_back) for ticker in tickers]
        self.weights = weights
        self.tickers = tickers
        self.ret = self.returns()
        self.volatility = np.std(self.ret)
        self.ave_return = np.mean(self.ret)
        self.sharpe = self.sharpe_ratio()
    

    def returns(self):
        returns = np.zeros(len(self.tickers[0].returns))
        j = 0
        for ticker in self.tickers:
            i = 0
            for val in ticker.returns:
                returns[i] = returns[i] + val*self.weights[j]
                i += 1
            j += 1
        return returns

    def sharpe_ratio(self, rfr=0.03):
        # rx - expected return
        # rf - risk free rate
        # std - volatility
        sharpe_ratio = (self.ave_return-rfr)/self.volatility
        return sharpe_ratio


class SharpeSimulation:
    def __init__(self, tickers, years_back, n):
        self.n = n
        self.years_back = years_back
        self.tickers = tickers
        self.weights = self.random_portfolio_weights()
        self.portfolios = self.simulate_portfolios()


    def random_portfolio_weights(self):
        num_tickers = len(self.tickers)
        weights = np.random.rand(self.n, num_tickers)
        for i in range(0, self.n):
            tot = sum(weights[i, 0:num_tickers])
            for j in range(0, num_tickers):
                weights[i, j] = weights[i, j] / tot
        return weights


    def simulate_portfolios(self):
        volatilities = np.zeros(self.n)
        expected_returns = np.zeros(self.n)
        sharpe_ratios = np.zeros(self.n)
        portfolios = [Portfolio(self.tickers, weight, self.years_back) for weight in self.weights]

        return portfolios

    def plot(self):
        sharpe_ratios = [portfolio.sharpe for portfolio in self.portfolios]
        expected_returns = [portfolio.ave_return for portfolio in self.portfolios]
        volatilities = [portfolio.volatility for portfolio in self.portfolios]


        plt.scatter(volatilities, expected_returns, c=sharpe_ratios, marker='s')
        plt.style.use('classic')
        # plt.title(title, fontsize=15)
        # rc('font', **{'family': 'serif', 'serif': ['Times']})
        # rc('text', usetex=True)
        plt.xlabel('Portfolio Volatility', fontsize=20)
        plt.ylabel('Expected Returns', fontsize=20)
        cb = plt.colorbar()
        cb.set_label('Sharpe Ratio')
        plt.tight_layout()
        plt.show()


    def max_sharpe(self):
        max_sr = 0
        for portfolio in self.portfolios:
            weights = portfolio.weights
            sr = portfolio.sharpe
            if sr > max_sr:
                max_sr = sr
                weights_final = weights
        return max_sr, weights_final



if __name__ == '__main__':


    tickers = ['SPY', 'QQQ', 'CRM', 'ARKK']
    n = 10000
    years_back = 6
    tickers = [Ticker(tick, years_back) for tick in tickers]
    sim = SharpeSimulation(tickers, years_back, n)


    max_sr, best_weights = sim.max_sharpe()

    print(max_sr, best_weights)

    sim.plot()




    