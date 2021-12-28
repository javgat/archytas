from __future__ import unicode_literals
import tweepy
import logging
import config
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Read JSON
f = open("auth_data.json", 'r')
data = json.load(f)
consumer_key = data['CONSUMER_KEY']
consumer_secret = data['CONSUMER_SECRET']
access_token = data['ACCESS_TOKEN']
access_token_secret = data['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#api.update_status("Soy un bot")
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

for tweet in list(tweepy.Cursor(api.search_tweets("#domingosanitario")).items(10)):
    try:
        print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

        tweet.retweet()
        print('Retweet published successfully.')

        # Where sleep(10), sleep is measured in seconds.
        # Change 10 to amount of seconds you want to have in-between retweets.
        # Read Twitter's rules on automation. Don't spam!
        sleep(1)

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepError as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error.reason)

    except StopIteration:
        break
