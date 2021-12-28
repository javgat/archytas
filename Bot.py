import tweepy
import json
import time

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

tweets = list(tweepy.Cursor(api.search_tweets,"#domingosanitario").items(30))
for tweet in tweets:
    try:
        print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

        tweet.retweet()
        print('Retweet published successfully.')

        # Read Twitter's rules on automation. Don't spam!
        time.sleep(2)

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepyException as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error)

    except StopIteration:
        break
