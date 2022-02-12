from model import TweetModel
from model import UserModel

from flask import g, jsonify


def tweet(request):
    user_tweet = request.json
    user_tweet['id'] = g.user_id

    tweet_content = user_tweet['tweet']

    if len(tweet_content) > 300:
        return '300자를 초과했습니다.', 400

    try:
        tweet_model = TweetModel()
        tweet_model.insert_tweet(user_tweet)
    except Exception as e:
        print(e)
        return 'insert tweet error', 400
    return '', 200


def follow(request):
    user_follow = request.json

    if 'id' not in user_follow.keys():
        user_follow['id'] = g.user_id

    try:
        tweet_model = TweetModel()
        tweet_model.insert_follow(user_follow)
    except Exception as e:
        print(e)
        return 'insert follow error', 400
    return '', 200


def unfollow(request):
    user_unfollow = request.json
    if 'id' not in user_unfollow.keys():
        user_unfollow['id'] = g.user_id
    try:
        tweet_model = TweetModel()
        tweet_model.insert_unfollow(user_unfollow)
    except Exception as e:
        print(e)
        return 'insert unfollow error', 400
    return '', 200


def timeline():
    user_id = g.user_id
    user_model = UserModel()
    tweet_model = TweetModel()

    try:
        user_info = user_model.get_user_from_id(user_id)
        time_line = tweet_model.get_timeline(user_id)

        print(time_line)
        time_line = [{
            'user_id': d[0],
            'tweet': d[1]
        } for d in time_line]

    except Exception as e:
        print(e)
        return '', 500

    return jsonify({
        'user_name': user_info['name'],
        'user_id': user_id,
        'timeline': time_line
    })
