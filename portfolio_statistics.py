import robin_stocks as rh
import pandas_datareader as web
import userFunctions as uf
from pprint import pprint
import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt

class Portfolio():

    def __init__(self):
        date = dt.date.today()
        date = date.strftime("%Y_%m_%d")

        # minimize API calls pulling data once per day
        if os.path.exists(f'portfolio_{date}.csv'):
            self.data = pd.read_csv(f'portfolio_{date}.csv')
        else:
            uf.login()
            self.data = pd.DataFrame(rh.get_historical_portfolio(interval='week', span='all')['equity_historicals'])
            self.data.to_csv(f'portfolio_{date}.csv')
            pprint(self.data)

        if os.path.exists(f'bank_transfers_{date}.csv'):
            self.bank_transfers = pd.read_csv(f'bank_transfers_{date}.csv')
        else:
            uf.login()
            self.bank_transfers = pd.DataFrame(rh.get_bank_transfers())
            self.bank_transfers.to_csv(f'bank_transfers_{date}.csv')

            for ix in self.bank_transfers.index:
                if self.bank_transfers.at[ix, 'direction'] == 'withdraw':
                    self.bank_transfers.at[ix, 'amount'] = -self.bank_transfers.at[ix, 'amount'] 

        pprint(self.bank_transfers)
        plt.plot(self.data['close_equity'])
        plt.show()

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