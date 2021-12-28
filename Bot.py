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
    auth = tweepy.OAuthHandler("6p7lkW7ZtDJEmiOnIrdJCsmJC", "mh9YWbWEGuQ0HpgHzaR2X8FMs2xVWQWkr0vcmp2AvXFncFFLy4")
    auth.set_access_token("558034177-4w5n7ZaMhKHvROvJPmq1eZtJsqiI1pYm1BeRmaEe", "lMWAApby7IWYkZs2L8ABBCfC3MgrJnpEor7UMsl3lwBXT")

    api = tweepy.API(auth)
    api.auth = auth
    #api.update_status("Soy un bot")
    tweets_listener = RetweetListener(api)
    stream = tweepy.Stream("6p7lkW7ZtDJEmiOnIrdJCsmJC","mh9YWbWEGuQ0HpgHzaR2X8FMs2xVWQWkr0vcmp2AvXFncFFLy4","558034177-4w5n7ZaMhKHvROvJPmq1eZtJsqiI1pYm1BeRmaEe","lMWAApby7IWYkZs2L8ABBCfC3MgrJnpEor7UMsl3lwBXT")
    stream.filter(track=keywords, languages=["es"])
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")



if __name__ == "__main__":
    main(["#domingosanitario"])
