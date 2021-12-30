import time
import csv
import random
import tweepy

def getTweetsKeyword(api: tweepy.API, keyword: str, items: int) -> list:
    tweets = list(tweepy.Cursor(api.search_tweets, keyword).items(items))
    return tweets

def retweetKeyword(api: tweepy.API, keyword: str, items: int, sleepSeconds: int):
    tweets = getTweetsKeyword(api, keyword, items)
    for tweet in tweets:
        try:
            print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

            tweet.retweet()
            print('Retweet published successfully.')

            # Read Twitter's rules on automation. Don't spam!
            time.sleep(sleepSeconds)

        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepyException as error:
            print('\nError TweepyException. Retweet not successful. Reason: ')
            print(error)

        except tweepy.HTTPException as error:
            print('\nError HTTPException. Retweet not successful. Reason: ')
            print(error)

        except StopIteration:
            break

def tweetRandom(api: tweepy.API, tweetsCSV: str, dailyTweets: int):
    # Read CSV
    with open(tweetsCSV, newline='') as f:
        reader = csv.reader(f)
        tweetData = list(reader)

    for _ in range(dailyTweets):
        try:
            api.update_status(random.choice(tweetData)[0])
        except:
            print("Already tweeted that")