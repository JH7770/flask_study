import jwt

from functools import wraps
from flask import request, Response, current_app, g

from .user import get_user_from_id


def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], "HS256")
    except jwt.InvalidTokenError:
        payload = None
    return payload



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            payload = check_access_token(access_token)
            if payload is None:
                return Response(status=401)
            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user_from_id(user_id) if user_id else None
        else:
            return Response(status=401)

        return f(*args, **kwagrs)

    return decorated_function

