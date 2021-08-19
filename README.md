# automated_stock_trading_and_analysis

## sharpe_ratio.py
Runs a Monte Carlo simulation for N number of random portfolios composed of a list of tickers for a specified number of years.
Plots all simulated portfolios and can return the maximum sharpe ratio and the ticker weights for the portfolio which this occurs. This is the "optimal" risk-adjusted portfolio.\
![sharpe_figure](https://user-images.githubusercontent.com/59593124/109966646-8318c080-7cbe-11eb-9bad-96757e89cc4c.png)


## black_scholes.py
Solves the Black-Scholes partial differential equation using the finite-difference method to estimate options pricing\
![Equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7B%5Cpartial%20V%7D%7B%5Cpartial%20t%7D%20&plus;%20%5Cfrac%7B1%7D%7B2%7D%5Csigma%20S%5E2%20%5Cfrac%7B%5Cpartial%5E2%20V%7D%7B%5Cpartial%20S%5E2%7D%20&plus;rS%5Cfrac%7B%5Cpartial%20V%7D%7B%5Cpartial%20S%7D%20-%20rV%20%3D%200)\
where V(t) is the option value, S(t) is the price of the underlying asset, t is time to expiration (with units of years), sigma is the volatility of the asset, and r is the risk free interest rate. \
![black_scholes3d](https://user-images.githubusercontent.com/59593124/109970138-b5c4b800-7cc2-11eb-8dc4-c4097ff1b758.png)\
![payoff_at_expiri](https://user-images.githubusercontent.com/59593124/109970199-c412d400-7cc2-11eb-919c-f4a022bc55fd.png)\


## geometric_brownian_motion.py
An assumption of the Black-Scholes PDE is that the price movement of the underlying security follows "geometric brownian motion" or a "random walk". This program simulates the stochastic differential equation driving brownian motion:\
![Equation](https://latex.codecogs.com/svg.image?S_t&space;=&space;S_0&space;exp((\mu&space;-&space;\frac{\sigma^2}{2})t&plus;\sigma&space;W_t)\

## charting_functions.py
Creates charts to give a high level overview of a Robinhood portfolio. Uses the robin-stocks package by jmfernandes.
Must create a config.json file in the format as follows:

```json
  {
    "username": "email@email.com",
    "password": "password123"
  }
  ```
  
![pct_return_bar](https://user-images.githubusercontent.com/59593124/109975204-684b4980-7cc8-11eb-8e23-11726fe63bf4.png)\
  
![portfolio_pie](https://user-images.githubusercontent.com/59593124/109975345-8ca72600-7cc8-11eb-93f7-ab08681f8ce2.png)\

![stocks_pie](https://user-images.githubusercontent.com/59593124/109975446-a0eb2300-7cc8-11eb-9ec1-d7b7cba691bf.png)\

## wallstreetbets.py
Counts mentions of tickers on r/wallstreetbets and creates a fund weighted by the number of mentions. Allows the ability to change the weight of mentions based on time periods of week, month, and year. 


