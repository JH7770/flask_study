from flask import Blueprint, render_template, request
from flask import redirect
from .common import check_access_token

bp = Blueprint("front", __name__, url_prefix="/")

import os

@bp.route('/', methods=['GET'])
def front_login():
    access_token = request.headers.get('Authorization')
    if access_token is not None:
        payload = check_access_token(access_token)
        if payload is not None:
            return redirect('/tweets')
    return render_template("login.html", API_URL=os.environ.get("API_URL")
)


#
# @bp.route('/login', methods=['GET'])
# def front_login2():
#     return render_template("login.html", API_URL="www.naver.com")


@bp.route('/tweets', methods=['GET'])
def front_tweet():
    return render_template('tweets.html', API_URL=os.environ.get("API_URL"))


@bp.route('/sign-up', methods=['GET'])
def front_sign_up():
    return render_template('signup.html', API_URL=os.environ.get("API_URL"))
