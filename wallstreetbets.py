import praw
import json
import robin_stocks as rh
from robin_stocks.helper import error_ticker_does_not_exist

ticker_file = open('tickers.csv', 'r')
tickers = ticker_file.read().splitlines()


keys_filename = 'reddit.json'
keys_file = open(keys_filename)
keys = json.load(keys_file)


reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['secret'],
                     username=keys['username'],
                     password=keys['password'],
                     user_agent='wsb')


subreddit = reddit.subreddit('wallstreetbets')

hot = subreddit.hot(limit=50)

for submission in hot:
    if not submission.stickied:
        print(submission.title)
