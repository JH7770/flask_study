import bcrypt
import jwt
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from flask import current_app
from services import user, tweet

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/sign-up", methods=['POST'])
def sign_up():
    """
    회원가입 API
    :return: 생성된 유저 정보
    """
    new_user = request.json
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('UTF-8'), bcrypt.gensalt()
    )
    new_user_id = user.insert_user(new_user)
    created_user = user.get_user_from_id(new_user_id)
    return jsonify(created_user)


@bp.route('/login', methods=['POST'])
def login():
    credential = request.json
    email = credential['email']
    password = credential['password']

    row = user.get_user_from_email(email)

    if row and bcrypt.checkpw(password.encode('UTF-8'),
                              row['hashed_password'].encode('UTF-8')):
        user_id = row['id']
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # expire 1 day
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], 'HS256')

        return jsonify({
            'user_id': user_id,
            'access_token': token.decode('UTF-8')
        })
    else:
        return '', 401
