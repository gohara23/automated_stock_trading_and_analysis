from genericpath import exists
import praw
import json
import robin_stocks as rh
import pandas as pd


# ticker_file = open('tickers.csv', 'r')
# tickers = ticker_file.read().splitlines()
tickers_df = pd.read_csv('tickers_header.csv')
tickers_df['count'] = 0
tickers_df.set_index('ticker', inplace=True)



keys_filename = 'reddit.json'
keys_file = open(keys_filename)
keys = json.load(keys_file)


reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['secret'],
                     username=keys['username'],
                     password=keys['password'],
                     user_agent='wsb')


subreddit = reddit.subreddit('wallstreetbets')

hot = subreddit.hot(limit=5)

# direct = dir(subreddit)
# for at in direct:
#     print(at)

top = subreddit.top('week', limit=5)
# direct = dir(top)
# for at in direct:
#     print(at)

for submission in top:
    print(submission.title)
    comments = submission.comments
    for comment in comments:
        for comment in comments:
            try:
                # print(20*'-')
                words = comment.body.split()
                for word in words:
                    if tickers_df.at[word, 'count'] >= 0:
                        tickers_df.at[word, 'count'] += 1
            except:
                pass

tickers_df.to_csv('ticker_counts.csv')
tickers_df.sort_values(by=['count'], ascending=False, inplace=True)
tot = tickers_df['count'].sum()
tickers_df['pct'] = [item / tot for item in tickers_df['count']]
print(tickers_df)

# for submission in hot:
#     if not submission.stickied:
#         print(submission.title)
#         comments = submission.comments
#         for comment in comments:
#             print(20*'-')
#             try:
#                 print(comment.body)
#             except:
#                 pass