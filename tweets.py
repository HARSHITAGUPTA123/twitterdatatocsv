# Read tweepy doc tutorials
# keys at (https://apps.twitter.com/app/13203717/keys)

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.max_columns = 50
pd.options.display.max_rows = 50
pd.options.display.width = 120

consumer_key = 'MW5tGq1YOCBmjdlHo7tmOGDRD'
consumer_secret = 'eAsIABSbTbSqyct9fZsaFvlQ1DXg1aIFkc8R36varJVCSaaWOF'
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

api = tweepy.API(auth)
results = api.search(q='demonetization')
print len(results)


def print_tweet(tweet):
    print "@%s - %s (%s)" % (tweet.user.screen_name, tweet.user.name, tweet.created_at)
    print tweet.text


tweet = results[0]
"""
for param in dir(tweet):
    if not param.startswith('_'):
        print '%s : %s' % (param,eval('tweet.' + param))
"""

user = tweet.author
"""
for param in dir(user):
    if not param.startswith('_'):
        print '%s : %s' % (param,eval('user.' + param))
"""

results = []
for tweet in tweepy.Cursor(api.search, q='demonetization').items(100):
    results.append(tweet)


def process_results(results):
    id_list = [tweet.id for tweet in results]
    df = pd.DataFrame(id_list, columns=['id'])
    df['text'] = [tweet.text for tweet in results]
    df['created_at'] = [tweet.created_at for tweet in results]
    df['retweet_count'] = [tweet.retweet_count for tweet in results]
    df['favorite_count'] = [tweet.favorite_count for tweet in results]
    df['source'] = [tweet.source for tweet in results]
    df['user_id'] = [tweet.author.id for tweet in results]
    df['user_screen_name'] = [tweet.author.screen_name for tweet in results]
    df['user_name'] = [tweet.author.name for tweet in results]
    df['user_created_at'] = [tweet.author.created_at for tweet in results]
    df['user_description'] = [tweet.author.description for tweet in results]
    df['user_followers_count'] = [tweet.author.followers_count for tweet in results]
    df['user_friends_count'] = [tweet.author.friends_count for tweet in results]
    df['user_location'] = [tweet.author.location for tweet in results]
    return df


df = process_results(results)

print df.head(5)

print df.tail(5)

df.to_csv('/home/harshita/web_scrapping/twitter/demon.csv', encoding='utf-8')

# [::-1] is for sorting and [:5] for top 5 sources
sources = df['source'].value_counts()[:5][::-1]

plt.barh(xrange(len(sources)), sources.values)
plt.yticks(np.arange(len(sources)) + 0.4, sources.index)
plt.show()
