import os
import tweepy
import pickle


def get_retweeters(api, tweet_id, retweeters_id_pickle, retweeters_pickle):
    """
    get retweeters id list of a tweet
    :param api:
    :param tweet_id:
    :param pickle_path:
    :return:
    """
    if os.path.exists(retweeters_id_pickle):
        with open(retweeters_id_pickle, 'rb') as f:
            retweeters_id = pickle.load(f)
    else:
        retweeters_id = api.retweeters(tweet_id)
        with open(retweeters_id_pickle, 'wb') as f:
            pickle.dump(retweeters_id, f)

    if os.path.exists(retweeters_pickle):
        with open(retweeters_pickle, 'rb') as f:
            retweeters = pickle.load(f)
    else:
        retweeters = api.statuses_lookup(retweeters_id)
        with open(retweeters_pickle, 'wb') as f:
            pickle.dump(retweeters, f)
    return retweeters


def get_friends_and_details(api, user_id):
    friends_details = api.friends(user_id)
    friends = [f.id for f in friends_details]
    return friends, friends_details


def get_followers_and_details(api, user_id):
    followers_details = api.followers(user_id)
    followers = [f.id for f in followers_details]
    return followers, followers_details









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

