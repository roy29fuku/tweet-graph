import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
import pickle

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


def get_retweeters(api, tweet_id, pickle_path):
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as f:
            retweeters = pickle.load(f)
    else:
        retweeters = api.retweeters(tweet_id)
        with open(pickle_path, 'wb') as f:
            pickle.dump(retweeters, f)
    return retweeters








def create_graph(tweet_id):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # get retweeters
    retweeter_ids = api.retweeters(tweet_id)
    print('retweeters: {}'.format(len(retweeter_ids)))

    # get follows and followers
    for user_id in retweeter_ids:
        friend_ids = api.friends_ids(user_id)
        follower_ids = api.followers_ids(user_id)

    print('friends: {}'.format(len(friends)))
    print('followers: {}'.format(len(followers)))

if __name__ == '__main__':
    tweet_id = '1134738254496800769'
    create_graph(tweet_id)

