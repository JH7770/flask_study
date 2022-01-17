from flask import Blueprint, request, jsonify
from services import tweet
from services.auth import login_required

bp = Blueprint("tweet", __name__, url_prefix="/")


@bp.route('/follow', methods=['POST'])
@login_required
def follow():
    """
    User Follow
    :return: 성공 여부
    """
    user_follow = request.json
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
    try:
        tweet.insert_unfollow(user_unfollow)
    except Exception as e:
        print(e)
        return 'insert unfollow error', 400
    return '', 200


@bp.route('/timeline/<int:user_id>', methods=['GET'])
@login_required
def timeline(user_id):
    """
    timeline을 받아옴
    :param user_id:
    :return:
    """
    time_line = tweet.get_timeline(user_id)
    return jsonify({
        'user_id': user_id,
        'timeline': time_line
    })
