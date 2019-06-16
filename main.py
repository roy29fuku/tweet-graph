import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
from create_graph import get_retweeters, get_friends, get_followers

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweet_id = '1134738254496800769'  # tweet id of roy29fuku
    retweeters = get_retweeters(api, tweet_id, 'data/retweeters_id.pickle', 'data/retweeters.pickle')

    user_id = '715433541375373312'  # user id of roy29fuku
    friends = get_friends(api, user_id, 'data/friends.pickle')
    followers = get_followers(api, user_id, 'data/followers.pickle')

