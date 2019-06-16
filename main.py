import os
from os.path import join, dirname
import csv
from dotenv import load_dotenv
import tweepy
import pickle
from tweet_graph import get_retweeters, get_friends, get_followers, compare_groups

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

    # 1. 特定のツイートをリツイートしたユーザ情報を取得
    tweet_id = '1134738254496800769'  # tweet id of roy29fuku
    retweeters = get_retweeters(api, tweet_id, 'data/retweeters_id.pickle', 'data/retweeters.pickle')

    # 2. 1のツイート発信者のフォロー（friends）、フォロワー情報を取得
    user_id = '715433541375373312'  # user id of roy29fuku
    friends = get_friends(api, user_id, 'data/friends.pickle')
    followers = get_followers(api, user_id, 'data/followers.pickle')

    # 3. フォロワーの中でリツイートしたユーザとリツイートしなかったユーザを比較分析（どのクラスタに刺さったか）
    # 　　もちろんリツイート後にフォローしたユーザもいる
    followers_rt = [f for f in followers if f in retweeters]
    followers_not_rt = [f for f in followers if f not in retweeters]
    groups = [followers_rt, followers_not_rt]
    files = ['data/followers_rt.png', 'data/followers_not_rt.png']
    compare_groups(groups, files)

    # 4. リツイートしてくれたユーザの中でフォローしていないユーザ
    retweeter_not_fl = [r for r in retweeters if r not in friends]
    with open('data/friend_candidates.csv', 'w') as f:
        writer = csv.writer(f)
        [writer.writerow([u.screen_name, u.description]) for u in retweeter_not_fl]

    # 5. グラフのリンクプレディクションで自分と繋がり得るユーザを探す
