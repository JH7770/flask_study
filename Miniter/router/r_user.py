from flask import Blueprint, request, jsonify
from services import user, tweet

bp = Blueprint("user", __name__, url_prefix="/")

@bp.route("/sign-up", methods=['POST'])
def sign_up():
    """
    회원가입 API
    :return: 생성된 유저 정보
    """
    new_user = request.json
    new_user_id = user.insert_user(new_user)
    created_user = user.get_user_from_id(new_user_id)
    return jsonify(created_user)



@bp.route('/tweet', methods=['POST'])
def tweet():
    """
    Tweet Upload
    :return: 성공 여부(status)
    """
    user_tweet = request.json
    tweet_content = user_tweet['tweet']

    if len(tweet_content) > 300:
        return '300자를 초과했습니다.', 400

    try:
        tweet.insert_tweet(user_tweet)
    except Exception as e:
        print(e)
        return 'insert tweet error', 400
    return '', 200

