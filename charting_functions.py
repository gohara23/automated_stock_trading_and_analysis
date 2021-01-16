import matplotlib.pyplot as plt
import userFunctions as uf
import pandas as pd
import robin_stocks as rh
import ast


def holding_pie():
    holdings = pd.DataFrame(rh.build_holdings())
    sizes = [holdings[item]['percentage'] for item in holdings]
    labels = [item for item in holdings]
    plt.style.use('classic')
    plt.rcParams["font.family"] = "serif"
    plt.tight_layout()
    plt.pie(sizes, labels=labels)
    plt.title('Portfolio Allocation', fontsize=20)
    plt.tight_layout()
    plt.show()
    return


def pct_return_bar():
    holdings = pd.DataFrame(rh.build_holdings())
    pct_change = [float(holdings[item]['percent_change']) for item in holdings]
    labels = [item for item in holdings]
    colors = ['g' if pct > 0 else 'r' for pct in pct_change]
    plt.bar(labels, pct_change, color=colors)
    plt.style.use('classic')
    plt.rcParams["font.family"] = "serif"
    plt.ylabel('Percent Return', fontsize=16)
    plt.tight_layout()
    plt.show()
    return


def get_options_exposure():
    opt = rh.get_open_option_positions()
    total_options_value = 0
    for item in opt:
        price = float(rh.get_option_market_data_by_id(
            item['option_id'])['adjusted_mark_price'])
        if item['type'] == 'short':
            total_options_value -= price
        else:
            total_options_value += price
    total_options_value *= 100
    return total_options_value


def get_crypto_exposure():
    crypto = rh.get_crypto_positions()
    exposure = 0
    for item in crypto:
        symbol = item['currency']['code']
        cost_basis = item['cost_bases'][0]
        quantity = float(cost_basis['direct_quantity'])
        current_price = float(rh.get_crypto_quote(symbol)['mark_price'])
        equity = current_price*quantity
        exposure += equity
    return exposure


def get_stock_exposure():
    holdings = rh.build_holdings()
    equity = 0
    for ticker in holdings:
        equity += float(holdings[ticker]['equity'])
    return equity


def asset_allocation():
    sizes = [get_options_exposure(), get_crypto_exposure(),
             get_stock_exposure()]
    labels = ['Options', 'Crypto', 'Stocks']
    colors = [(0.1, 0.9, 0.9, 1.0), (0.5, 0.5, 0.5, 0.5),
              (0.0, 1.0, 0.45, 1.0)]
    plt.style.use('classic')
    plt.rcParams["font.family"] = "serif"
    plt.tight_layout()
    plt.pie(sizes, labels=labels, colors=colors)
    plt.title('Portfolio Allocation', fontsize=20)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    uf.login()
    asset_allocation()
