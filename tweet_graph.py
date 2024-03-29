import os
import pickle
from time import sleep
from tqdm import tqdm
from wordcloud import WordCloud
import MeCab


def get_retweeters(api, tweet_id, retweeters_id_pickle, retweeters_pickle):
    """
    get retweeters of a tweet
    :param api:
    :param tweet_id:
    :param retweeters_id_pickle:
    :param retweeters_pickle:
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
        retweeters = []
        for rid in tqdm(retweeters_id):
            retweeters.append(api.get_user(rid))
            sleep(60)
        with open(retweeters_pickle, 'wb') as f:
            pickle.dump(retweeters, f)

    return retweeters


def get_friends(api, user_id, friends_id_pickle, friends_pickle):
    """
    get friend of a user
    :param api:
    :param user_id:
    :param friends_pickle:
    :return:
    """
    if os.path.exists(friends_id_pickle):
        with open(friends_id_pickle, 'rb') as f:
            friends_id = pickle.load(f)
    else:
        friends_id = api.friends_ids(user_id)
        with open(friends_id_pickle, 'wb') as f:
            pickle.dump(friends_id, f)

    if os.path.exists(friends_pickle):
        with open(friends_pickle, 'rb') as f:
            friends = pickle.load(f)
    else:
        friends = []
        for fid in tqdm(friends_id):
            friends.append(api.get_user(fid))
            sleep(60)
        with open(friends_pickle, 'wb') as f:
            pickle.dump(friends, f)

    return friends


def get_followers(api, user_id, followers_id_pickle, followers_pickle):
    """
    get followers of a user
    :param api:
    :param user_id:
    :param followers_picke:
    :return:
    """
    if os.path.exists(followers_id_pickle):
        with open(followers_id_pickle, 'rb') as f:
            followers_id = pickle.load(f)
    else:
        followers_id = api.followers_ids(user_id)
        with open(followers_id_pickle, 'wb') as f:
            pickle.dump(followers_id, f)

    if os.path.exists(followers_pickle):
        with open(followers_pickle, 'rb') as f:
            followers = pickle.load(f)
    else:
        followers = []
        for fid in tqdm(followers_id):
            followers.append(api.get_user(fid))
            sleep(60)
        with open(followers_pickle, 'wb') as f:
            pickle.dump(followers, f)

    return followers


def create_word_cloud(text, file, color='white',
                      font_path='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc',
                      width=1024, height=674):
    """
    :param text:
    :param file:
    :param color:
    :param font_path:
    :param width:
    :param height:
    :return:
    """
    wordcloud = WordCloud(background_color=color,
                          font_path=font_path,
                          width=width, height=height).generate(text)
    wordcloud.to_file(file)
    return


def compare_groups(groups, files):
    """
    :param groups:
    :return:
    """
    tagger = MeCab.Tagger('')
    tagger.parse('')
    for group, file in zip(groups, files):
        description = ' '.join([user.description for user in group])
        node = tagger.parseToNode(description)
        words = []
        while node:
            words.append(node.surface)
            node = node.next
        create_word_cloud(' '.join(words), file)
    return


def create_graph(api, tweet_id):
    # get retweeters
    retweeter_ids = api.retweeters(tweet_id)
    print('retweeters: {}'.format(len(retweeter_ids)))

    # get follows and followers
    for user_id in retweeter_ids:
        friend_ids = api.friends_ids(user_id)
        follower_ids = api.followers_ids(user_id)

    print('friends: {}'.format(len(friends)))
    print('followers: {}'.format(len(followers)))

