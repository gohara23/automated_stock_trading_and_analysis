import praw
import json
import pandas as pd


''' Counts mentions of tickers on r/wallstreetbets and for top posts
    of the week, month, and year. Weights the tickers accordingly '''


def get_fund_weights(week_weight=0.25, month_weight=0.25, year_weight=0.5, num_posts=1000):

    tickers_df = pd.read_csv('tickers_header.csv')
    tickers_df['count_week'] = 0
    tickers_df['count_month'] = 0
    tickers_df['count_year'] = 0
    tickers_df['pct_week'] = 0
    tickers_df['pct_month'] = 0
    tickers_df['pct_year'] = 0
    tickers_df['fund_weights'] = 0
    tickers_df.set_index('ticker', inplace=True)

    keys_filename = 'reddit.json'
    keys_file = open(keys_filename)
    keys = json.load(keys_file)

    reddit = praw.Reddit(client_id=keys['client_id'],
                         client_secret=keys['secret'],
                         username=keys['username'],
                         password=keys['password'],
                         user_agent='wsb')

    wsb = reddit.subreddit('wallstreetbets')

    top_week = wsb.top('week', limit=num_posts)
    top_month = wsb.top('month', limit=num_posts)
    top_year = wsb.top('year', limit=num_posts)

    for submission in top_week:
        comments = submission.comments
        for comment in comments:
            try:
                words = comment.body.split()
                for word in words:
                    if tickers_df.at[word, 'count_week'] >= 0:
                        tickers_df.at[word, 'count_week'] += 1
            except:
                pass

    for submission in top_month:
        comments = submission.comments
        for comment in comments:
            try:
                words = comment.body.split()
                for word in words:
                    if tickers_df.at[word, 'count_month'] >= 0:
                        tickers_df.at[word, 'count_month'] += 1
            except:
                pass

    for submission in top_year:
        comments = submission.comments
        for comment in comments:
            try:
                words = comment.body.split()
                for word in words:
                    if tickers_df.at[word, 'count_year'] >= 0:
                        tickers_df.at[word, 'count_year'] += 1
            except:
                pass

    tot_week = tickers_df['count_week'].sum()
    tickers_df['pct_week'] = [
        item / tot_week for item in tickers_df['count_week']]

    tot_month = tickers_df['count_month'].sum()
    tickers_df['pct_month'] = [
        item / tot_month for item in tickers_df['count_month']]

    tot_year = tickers_df['count_year'].sum()
    tickers_df['pct_year'] = [
        item / tot_year for item in tickers_df['count_year']]


    tickers_df['fund_weights'] = [tickers_df.at[ticker, 'pct_week']*week_weight + tickers_df.at[ticker, 'pct_month']
                                  * month_weight + tickers_df.at[ticker, 'pct_year']*year_weight for ticker in tickers_df.index]

    tickers_df.sort_values(by=['fund_weights'], ascending=False, inplace=True)

    # Drop Tickers with no mentions
    for ticker in tickers_df.index:
        if tickers_df.at[ticker, 'fund_weights'] == 0:
            tickers_df.drop([ticker], inplace=True)

    return tickers_df


data = get_fund_weights()
print(data)
data.to_csv('fund_weights.csv')



