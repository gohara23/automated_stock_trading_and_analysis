import matplotlib.pyplot as plt 
import userFunctions as uf 
import pandas as pd 
import robin_stocks as rh 

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