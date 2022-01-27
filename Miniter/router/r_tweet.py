from flask import Blueprint, request, jsonify, g
from services import tweet
from services import user
from services.auth import login_required

bp = Blueprint("tweet", __name__, url_prefix="/tweet")

@bp.route('/tweet', methods=['POST'])
@login_required
def _tweet():
    """
    Tweet Upload
    :return: 성공 여부(status)
    """
    user_tweet = request.json
    user_tweet['id'] = g.user_id
    tweet_content = user_tweet['tweet']

    if len(tweet_content) > 300:
        return '300자를 초과했습니다.', 400

    try:
        tweet.insert_tweet(user_tweet)
    except Exception as e:
        print(e)
        return 'insert tweet error', 400
    return '', 200


@bp.route('/follow', methods=['POST'])
@login_required
def follow():
    """
    User Follow
    :return: 성공 여부
    """
    user_follow = request.json

    if 'id' not in user_follow.keys():
        user_follow['id'] = g.user_id
    try:
        tweet.insert_follow(user_follow)
    except Exception as e:
        print(e)
        return 'insert follow error', 400
    return '', 200


@bp.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    """
    User UnFollow
    :return: 성공 여부
    """
    user_unfollow = request.json
    if 'id' not in user_unfollow.keys():
        user_unfollow['id'] = g.user_id
    try:
        tweet.insert_unfollow(user_unfollow)
    except Exception as e:
        print(e)
        return 'insert unfollow error', 400
    return '', 200


@bp.route('/timeline', methods=['GET'])
@login_required
def timeline():
    """
    timeline을 받아옴
    :param user_id:
    :return:
    """
    user_id = g.user_id
    user_info = user.get_user_from_id(user_id)
    time_line = tweet.get_timeline(user_id)
    return jsonify({
        'user_name': user_info['name'],
        'user_id': user_id,
        'timeline': time_line
    })
