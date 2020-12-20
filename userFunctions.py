import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style 
import pandas as pd 
import pandas_datareader.data as web 
import robin_stocks as rh
import json
import os


def closePrice(ticker = str, date = str):
    ## Returns the close price for a ticker at a specified date as a float
    closePrice = web.DataReader(ticker, 'yahoo', date, date)['Adj Close']
    try: 
        closePrice = round(float(closePrice), 2)
    except:
        try:
            date2 = dt.datetime.strptime(date, '%Y-%m-%d')
            date2 = date2 + dt.timedelta(1)
            date2 = date2.strftime('%Y-%m-%d')
            print(date2)
            closePrice = web.DataReader(ticker, 'yahoo', date2, date2)['Adj Close']
            closePrice = round(float(closePrice), 2)
        except: 
            try:
                date2 = dt.datetime.strptime(date, '%Y-%m-%d')
                date2 = date2 + dt.timedelta(-2)
                date2 = date2.strftime('%Y-%m-%d')
                print(date2)
                closePrice = web.DataReader(ticker, 'yahoo', date2, date2)['Adj Close']
                closePrice = round(float(closePrice), 2)
            except:
                closePrice = 'Err'
    return closePrice



## Count of how many open options for ticker
def optionsCount(ticker):
    optionsCount = 0
    openOptions = rh.options.get_open_option_positions('chain_symbol')
    for item in openOptions:
        if item == ticker:
            optionsCount = optionsCount +1
    return optionsCount

## Get current price as a float
def priceFloat(ticker):
    currentPrice = rh.get_latest_price(ticker)
    for item in currentPrice:
        currentPrice = float(item)
    return currentPrice

## Login
def login():
    content = open('config.json').read()
    config = json.loads(content)
    rh.login(config["username"], config["password"])

## Rounding 
def round_of_rating(number):
    return round(number * 2) / 2

## Convert to float
def floatConvert(element):
    for item in element:
        element = float(item)
    return element

## Convert to String
def stringConvert(element):
    for item in element:
        element = str(item)
    return element

def optionbyDelta(ticker, expirationDate, targetDelta, opType):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    for index, row in chains.iterrows():
        itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
    print('strike')
    print(targetStrike)
    print('id')
    print(targetID)
    print('real delta')
    print(realDelta)
    return targetID, targetStrike

def optionbyDeltaVertical(ticker, expirationDate, targetDelta, opType):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    for index, row in chains.iterrows():
        itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
            rowShort = row
    priceErrorLast = 2
    targetStrike = float(targetStrike)
    for index, row in chains.iterrows():
        itPrice = float(row['strike_price'])
        errorAbs = abs(itPrice-targetStrike)
        errorTrue = itPrice - targetStrike
        if errorAbs < priceErrorLast and errorTrue > 0:
            targetIDlong = row['id']
            targetStrikelong = row['strike_price']
            realDeltalong = row['delta']
            priceErrorLast = errorAbs
            rowLong = row   
    print('strike')
    print(targetStrike)
    print('id')
    print(targetID)
    print('real delta')
    print(realDelta)

    print('long strike price')
    print(targetStrikelong)
    print('long id')
    print(targetIDlong)
    print('long row:', rowLong)
    print('short row', rowShort['state'])
    return targetID, targetStrike, targetIDlong, targetStrikelong

def callCreditinfo(ticker, expirationDate, targetDelta, opType):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    for index, row in chains.iterrows():
        if row['delta'] is None :
            row['delta'] = float(0)
            itDelt = float(row['delta'])
        else:
            itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
            rowShort = row
    priceErrorLast = 2
    targetStrike = float(targetStrike)
    for index, row in chains.iterrows():
        itPrice = float(row['strike_price'])
        errorAbs = abs(itPrice-targetStrike)
        errorTrue = itPrice - targetStrike
        if errorAbs < priceErrorLast and errorTrue > 0:
            targetIDlong = row['id']
            targetStrikelong = row['strike_price']
            realDeltalong = row['delta']
            priceErrorLast = errorAbs
            rowLong = row   
    return rowLong, rowShort

def putCreditinfo(ticker, expirationDate, targetDelta, opType):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    chains.to_csv('msftPutCred.csv') 
    for index, row in chains.iterrows():
        if row['delta'] is None :
            row['delta'] = float(0)
            itDelt = float(row['delta'])
        else:
            itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
            rowShort = row
    priceErrorLast = 4
    targetStrike = float(targetStrike)
    for index, row in chains.iterrows():
        itPrice = float(row['strike_price'])
        errorAbs = abs(itPrice-targetStrike)
        errorTrue = itPrice - targetStrike
        if errorAbs < priceErrorLast and errorTrue < 0:
            targetIDlong = row['id']
            targetStrikelong = row['strike_price']
            realDeltalong = row['delta']
            priceErrorLast = errorAbs
            rowLong = row   
    return rowLong, rowShort

def daysOut(ticker, targetDays):
    today = dt.date.today()
    targetExpiration = today + dt.timedelta(targetDays)
    targetExpiration = str(targetExpiration)
    chains = rh.find_options_for_stock_by_expiration(ticker, targetExpiration, 'call')
    #chains = pd.DataFrame(chains)
    print(chains[0])
    n=1
    while chains[0] is None:
        targetExpiration = today + dt.timedelta(targetDays-n)
        targetExpiration = str(targetExpiration)
        chains = rh.find_options_for_stock_by_expiration(ticker, targetExpiration, 'call')    
        n = n + 1
    return targetExpiration

def optionsCountorders(ticker):
    optionsCount = 0
    openOptions = rh.options.get_open_option_positions('chain_symbol')
    openOrders = rh.get_all_open_orders('chain_symbol')
    for item in openOptions:
        if item == ticker:
            optionsCount = optionsCount +1
    for item in openOrders:
        if item == ticker:
            optionsCount = optionsCount +1
    return optionsCount

## Get Data from Yahoo Finance (for VIX)
def yahooPrice(ticker):
    start = str(dt.date.today()-dt.timedelta(4))
    end = str(dt.date.today())
    price = web.DataReader(ticker, 'yahoo', start, end)
    price = price['Close']
    price = float(price.tail(1))
    return price

def fridayExpiri(ticker, targetDays):
    today = dt.date.today()
    targetExpiration = today + dt.timedelta(targetDays)
    while targetExpiration.weekday() != 4:
        targetExpiration = targetExpiration + dt.timedelta(1)

    return str(targetExpiration)

def wedExpiri(ticker, targetDays):
    today = dt.date.today()
    targetExpiration = today + dt.timedelta(targetDays)
    while targetExpiration.weekday() != 2:
        targetExpiration = targetExpiration + dt.timedelta(1)

    return str(targetExpiration)



## Functions to Place Orders:
def sell_ironCondor(ticker = str, expirationDate = str, delta = float, callWeight = 1, putWeight = 1):
    callDelta = delta
    putDelta = -delta
    ## Get Put Credit Spread Info
    putInfo = putCreditinfo(ticker, expirationDate, putDelta, 'put')
    shortPutInfo = putInfo[1]
    longPutInfo = putInfo[0]
    shortPutStrike = str(round(float(shortPutInfo['strike_price']), 1))
    longPutStrike = str(round(float(longPutInfo['strike_price']), 1))
    longPutprice = float(longPutInfo['high_fill_rate_buy_price'])
    shortPutprice = float(shortPutInfo['high_fill_rate_buy_price'])
    putSpreadPrice = round(abs(shortPutprice-longPutprice), 2)
    longPut = {"expirationDate": expirationDate,
        "strike":longPutStrike,
        "optionType":"put",
        "effect":"open",
        "action":"buy"}

    shortPut = {"expirationDate": expirationDate,
            "strike": shortPutStrike,
            "optionType":"put",
            "effect":"open",
            "action":"sell"}

    putCreditspread = [longPut, shortPut]

    ## Get Call Credit Info
    callInfo = callCreditinfo(ticker, expirationDate, callDelta, 'call')
    shortCallInfo = callInfo[1]
    longCallInfo = callInfo[0]
    shortCallStrike = str(round(float(shortCallInfo['strike_price']), 1))
    longCallStrike = str(round(float((longCallInfo['strike_price'])), 1))
    longCallprice = float(longCallInfo['high_fill_rate_buy_price'])
    shortCallprice = float(shortCallInfo['high_fill_rate_sell_price'])
    price = round(abs(shortCallprice-longCallprice),2)

    longCall = {"expirationDate": expirationDate,
            "strike":longCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"buy"}

    shortCall = {"expirationDate": expirationDate,
            "strike": shortCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"sell"}

    callCreditspread = [longCall, shortCall]
    ## Print Summary Info Before Placing Order
    print('shortPutStrike...', shortPutStrike)
    print('longPutStrike...', longPutStrike)
    print('shortCallStrike...', shortCallStrike)
    print('longCallStrike...', longCallStrike)
    ## Place Orders
    callCredit = rh.order_option_spread('credit', price, ticker, callWeight, callCreditspread)
    print(callCredit)
    putCredit = rh.order_option_spread('credit', putSpreadPrice, ticker, putWeight, putCreditspread)
    print(putCredit)

def putCreditSpread(ticker = str, expirationDate = str, delta = float, qty =1):
    ## Make sure delta is negative
    if delta > 0:
        delta = -delta
    ## Get Put Credit Spread Info
    putInfo = putCreditinfo(ticker, expirationDate, delta, 'put')
    shortPutInfo = putInfo[1]
    longPutInfo = putInfo[0]
    shortPutStrike = str(round(float(shortPutInfo['strike_price']), 1))
    longPutStrike = str(round(float(longPutInfo['strike_price']), 1))
    longPutprice = float(longPutInfo['high_fill_rate_buy_price'])
    shortPutprice = float(shortPutInfo['high_fill_rate_buy_price'])
    putSpreadPrice = round(abs(shortPutprice-longPutprice), 2)
    longPut = {"expirationDate": expirationDate,
        "strike":longPutStrike,
        "optionType":"put",
        "effect":"open",
        "action":"buy"}
    shortPut = {"expirationDate": expirationDate,
            "strike": shortPutStrike,
            "optionType":"put",
            "effect":"open",
            "action":"sell"}
    putCreditspread = [longPut, shortPut]
    ## Place Order and Print Summary
    putCredit = rh.order_option_spread('credit', putSpreadPrice, ticker, qty , putCreditspread)
    print(putCredit)
    print('shortPutStrike...', shortPutStrike)
    print('longPutStrike...', longPutStrike)

def callCreditSpread(ticker = str, expirationDate = str, delta = float, qty =1):
    ## Get Call Credit Info
    callInfo = callCreditinfo(ticker, expirationDate, delta, 'call')
    shortCallInfo = callInfo[1]
    longCallInfo = callInfo[0]
    shortCallStrike = str(round(float(shortCallInfo['strike_price']), 1))
    longCallStrike = str(round(float((longCallInfo['strike_price'])), 1))
    longCallprice = float(longCallInfo['high_fill_rate_buy_price'])
    shortCallprice = float(shortCallInfo['high_fill_rate_sell_price'])
    price = round(abs(shortCallprice-longCallprice),2)
    longCall = {"expirationDate": expirationDate,
            "strike":longCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"buy"}
    shortCall = {"expirationDate": expirationDate,
            "strike": shortCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"sell"}
    callCreditspread = [longCall, shortCall]
    ## Place Order and Print Summary
    callCredit = rh.order_option_spread('credit', price, ticker, qty, callCreditspread)
    print(callCredit)
    print('shortCallStrike...', shortCallStrike)
    print('longCallStrike...', longCallStrike)

def callDebitSpread(ticker = str, expirationDate = str, delta = float, qty =1):
    ## Get Call Debit Info
    callInfo = callDebitinfo(ticker, expirationDate, delta, 'call')
    shortCallInfo = callInfo[1]
    longCallInfo = callInfo[0]
    shortCallStrike = str(round(float(shortCallInfo['strike_price']), 1))
    longCallStrike = str(round(float((longCallInfo['strike_price'])), 1))
    longCallprice = float(longCallInfo['high_fill_rate_buy_price'])
    shortCallprice = float(shortCallInfo['high_fill_rate_sell_price'])
    price = round(abs(shortCallprice-longCallprice),2)
    longCall = {"expirationDate": expirationDate,
            "strike":longCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"buy"}
    shortCall = {"expirationDate": expirationDate,
            "strike": shortCallStrike,
            "optionType":"call",
            "effect":"open",
            "action":"sell"}
    callCreditspread = [longCall, shortCall]
    ## Place Order and Print Summary
    callCredit = rh.order_option_spread('debit', price, ticker, qty, callCreditspread)
    print(callCredit)
    print('shortCallStrike...', shortCallStrike)
    print('longCallStrike...', longCallStrike)

def putDebitSpread(ticker = str, expirationDate = str, delta = float, qty =1):
    ## Make sure delta is negative
    if delta > 0:
        delta = -delta
    ## Get Put Credit Spread Info
    putInfo = putDebitInfo(ticker, expirationDate, delta, 'put')
    longPutInfo = putInfo[0]
    shortPutInfo = putInfo[1]
    shortPutStrike = str(round(float(shortPutInfo['strike_price']), 1))
    longPutStrike = str(round(float(longPutInfo['strike_price']), 1))
    longPutprice = float(longPutInfo['high_fill_rate_buy_price'])
    shortPutprice = float(shortPutInfo['high_fill_rate_buy_price'])
    putSpreadPrice = round(abs(shortPutprice-longPutprice), 2)
    longPut = {"expirationDate": expirationDate,
        "strike":longPutStrike,
        "optionType":"put",
        "effect":"open",
        "action":"buy"}
    shortPut = {"expirationDate": expirationDate,
            "strike": shortPutStrike,
            "optionType":"put",
            "effect":"open", 
            "action":"sell"}
    putCreditspread = [longPut, shortPut]
    ## Place Order and Print Summary
    putCredit = rh.order_option_spread('debit', putSpreadPrice, ticker, qty , putCreditspread)
    print(putCredit)
    print('shortPutStrike...', shortPutStrike)
    print('longPutStrike...', longPutStrike)

def callDebitinfo(ticker, expirationDate, targetDelta, opType):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    for index, row in chains.iterrows():
        if row['delta'] is None :
            row['delta'] = float(0)
            itDelt = float(row['delta'])
        else:
            itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
            rowShort = row
    priceErrorLast = 2
    targetStrike = float(targetStrike)
    for index, row in chains.iterrows():
        itPrice = float(row['strike_price'])
        errorAbs = abs(itPrice-targetStrike)
        errorTrue = itPrice - targetStrike
        if errorAbs < priceErrorLast and errorTrue < 0:
            targetIDlong = row['id']
            targetStrikelong = row['strike_price']
            realDeltalong = row['delta']
            priceErrorLast = errorAbs
            rowLong = row   
    return rowLong, rowShort

def putDebitInfo(ticker, expirationDate, targetDelta, opType = 'put'):
    errorLast = 1
    chains = rh.find_options_for_stock_by_expiration(ticker, expirationDate, opType)
    chains = pd.DataFrame(chains)
    for index, row in chains.iterrows():
        if row['delta'] is None :
            row['delta'] = float(0)
            itDelt = float(row['delta'])
        else:
            itDelt = float(row['delta'])
        error = abs(itDelt-targetDelta)
        if error < errorLast:
            targetID = row['id']
            targetStrike = row['strike_price']
            realDelta = row['delta']
            errorLast = error
            rowShort = row
    priceErrorLast = 2
    targetStrike = float(targetStrike)
    for index, row in chains.iterrows():
        itPrice = float(row['strike_price'])
        errorAbs = abs(itPrice-targetStrike)
        errorTrue = itPrice - targetStrike
        if errorAbs < priceErrorLast and errorTrue > 0:
            targetIDlong = row['id']
            targetStrikelong = row['strike_price']
            realDeltalong = row['delta']
            priceErrorLast = errorAbs
            rowLong = row   
    return rowLong, rowShort

def buy_ironCondor(ticker = str, expirationDate = str, delta = float, callWeight = 1, putWeight = 1):
    callDebitSpread(ticker, expirationDate, delta, callWeight)
    putDebitSpread(ticker, expirationDate, delta, putWeight)

def sell_ironCondor_byDelta(ticker = str, expirationDate = str, callDelta = float, putDelta=float, callWeight = 1, putWeight = 1):
    callCreditSpread(ticker, expirationDate, callDelta, callWeight)
    putCreditSpread(ticker, expirationDate, putDelta, putWeight)


## Bollinger Bands ##

def topBollinger(ticker = str):
    # Arbitrary Start and End Dates
    start = dt.datetime(2015,1,1)
    end = dt.datetime.now()
    ## Get data from yahoo finance
    msft = web.DataReader(ticker, 'yahoo', start, end)
    msftClose = msft['Adj Close']
    msft20dma = msftClose.rolling(window=20).mean()
    msftSTD = msftClose.rolling(window = 20).std()
    topBand = msft20dma + 2 * msftSTD
    bottomBand = msft20dma - 2 * msftSTD
    ## Get last data point on moving average
    topIndicator = round(float(topBand.tail(1)), 2)
    return topIndicator

def bottomBollinger(ticker = str):
    # Arbitrary Start and End Dates
    start = dt.datetime(2017,1,1)
    end = dt.datetime.now()
    ## Get data from yahoo finance
    msft = web.DataReader(ticker, 'yahoo', start, end)
    msftClose = msft['Adj Close']
    msft20dma = msftClose.rolling(window=20).mean()
    msftSTD = msftClose.rolling(window = 20).std()
    topBand = msft20dma + 2 * msftSTD
    bottomBand = msft20dma - 2 * msftSTD
    ## Get last data point on moving average
    bottomIndicator = round(float(bottomBand.tail(1)), 2)
    return bottomIndicator

def topBollinger_timeSeries(ticker, start, end):
    prices = web.DataReader(ticker, 'yahoo', start, end)
    ticker_close = prices['Adj Close']
    ticker_20dma = ticker_close.rolling(window = 20).mean()
    ticker_std = ticker_close.rolling(window = 20).std()
    ticker_topBand = ticker_20dma + 2 * ticker_std
    return ticker_topBand

def bottomBollinger_timeSeries(ticker, start, end):
    prices = web.DataReader(ticker, 'yahoo', start, end)
    ticker_close = prices['Adj Close']
    ticker_20dma = ticker_close.rolling(window = 20).mean()
    ticker_std = ticker_close.rolling(window = 20).std()
    ticker_bottomBand = ticker_20dma - 2 * ticker_std
    return ticker_bottomBand

def midBollinger_timeSeries(ticker, start, end):
    prices = web.DataReader(ticker, 'yahoo', start, end)
    ticker_close = prices['Adj Close']
    ticker_20dma = ticker_close.rolling(window = 20).mean()
    return ticker_20dma

## Days Until Next Earnings ##
def daysToEarnings(symbol = str):
    today = dt.date.today()
    earnings = rh.get_earnings(symbol)
    earnings = pd.DataFrame(earnings)
    report = earnings.report
    daysUntil = 100
    for item in report:
        date = dt.datetime.strptime(str(item['date']), '%Y-%m-%d')
        date = date.date()
        td = date - today
        td = td.days
        if td < daysUntil and td > 0 :
            daysUntil = td
    return int(daysUntil)


## .txt Symbol List ##
def symbolList(txtFile = str):
    data = open(txtFile)
    symbols = data.read().splitlines()
    return symbols

## List Days to Earnings ##
def list_daysToEarnings(tickers = list):
    for item in tickers:
        days = daysToEarnings(item)
        print(item, '...', days)

## Enter Directory 
def pi_data_directory():
    path = os.getcwd()
    os.chdir('%s/%s' % (path, 'piOptionsChainDataGrabber'))

## Function to change Date format from mmmm dd, yyyy to yyyy-mm-dd##
def dateChange(ticker_dates):
    for date in ticker_dates:
        loc = ticker_dates.index(date)
        date = dt.datetime.strptime(date, "%B %d, %Y")
        date = dt.datetime.strftime(date, '%Y-%m-%d')
        ticker_dates[loc]= date
    return ticker_dates