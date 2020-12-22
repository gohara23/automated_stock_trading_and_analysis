import praw
import json 

keys_filename = 'reddit.json'
keys_file = open(keys_filename)
keys = json.load(keys_file)


reddit = praw.Reddit(client_id=keys['client_id'] ,
                    client_secret=keys['secret'] ,
                    username= keys['username'],
                    password= keys['password'],
                    user_agent= 'wsb')



subreddit = reddit.subreddit('wallstreetbets')

hot = subreddit.hot(limit=10)

for submission in hot:
    print(submission.title)