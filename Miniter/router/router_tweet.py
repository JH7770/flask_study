from flask import Blueprint, request, jsonify, g
from services import service_tweet
from services import service_user
from .common import login_required

bp = Blueprint("tweet", __name__, url_prefix="/tweet")

@bp.route('/tweet', methods=['POST'])
@login_required
def _tweet():
    """
    Tweet Upload
    :return: 성공 여부(status)
    """

    return service_tweet.tweet(request)

@bp.route('/follow', methods=['POST'])
@login_required
def follow():
    """
    User Follow
    :return: 성공 여부
    """
    return service_tweet.follow(request)


@bp.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    """
    User UnFollow
    :return: 성공 여부
    """
    return service_tweet.unfollow(request)


@bp.route('/timeline', methods=['GET'])
@login_required
def timeline():
    """
    timeline을 받아옴
    :param user_id:
    :return:
    """
    return service_tweet.timeline()