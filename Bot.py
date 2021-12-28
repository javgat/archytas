from __future__ import unicode_literals
import tweepy
import logging
import config
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetListener(tweepy.Stream):
    def __init__(self, api):
        self.api = api
    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
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
    tweets_listener = RetweetListener(api)
    stream = tweepy.Stream(consumer_key,consumer_secret,access_token,access_token_secret)
    stream.filter(track=keywords, languages=["es"])
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

if __name__ == "__main__":
    main(["#domingosanitario"])
