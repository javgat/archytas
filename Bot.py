import tweepy
import json
import time
import csv
import random

class AuthData:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    @staticmethod
    def CreateFromJson(fileLocation: str) -> 'AuthData': 
        f = open(fileLocation, 'r')
        data = json.load(f)
        consumer_key = data['CONSUMER_KEY']
        consumer_secret = data['CONSUMER_SECRET']
        access_token = data['ACCESS_TOKEN']
        access_token_secret = data['ACCESS_TOKEN_SECRET']
        return AuthData(consumer_key, consumer_secret, access_token, access_token_secret)

def retweetKeyword(api: tweepy.API, keyword: str, items: int):
    tweets = list(tweepy.Cursor(api.search_tweets, keyword).items(items))
    for tweet in tweets:
        try:
            print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

            tweet.retweet()
            print('Retweet published successfully.')

            # Read Twitter's rules on automation. Don't spam!
            time.sleep(2)

        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepyException as error:
            print('\nError TweepyException. Retweet not successful. Reason: ')
            print(error)

        except tweepy.HTTPException as error:
            print('\nError HTTPException. Retweet not successful. Reason: ')
            print(error)

        except StopIteration:
            break

def main():
    # Read auth data
    ad = AuthData.CreateFromJson("auth_data.json")
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(ad.consumer_key, ad.consumer_secret)
    auth.set_access_token(ad.access_token, ad.access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    
    dailyTweets = 3
    # Read CSV
    with open('tweets.csv', newline='') as f:
        reader = csv.reader(f)
        tweetData = list(reader)

    for i in range(dailyTweets):
        try:
            api.update_status(random.choice(tweetData)[0])
        except:
            print("Already tweeted that")
    
    # Retweet some tweets with the hashtag
    retweetKeyword(api, "#domingosanitario", 30)

if __name__=="__main__":
    main()