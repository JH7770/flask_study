import os
import bcrypt
import jwt
from datetime import datetime, timedelta

from flask import current_app, jsonify, g, send_file
from model import UserModel
from common import s3

from werkzeug.utils import secure_filename

def sign_up(request):
    new_user = request.json
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('UTF-8'), bcrypt.gensalt()
    )
    user_model = UserModel()
    try:
        new_user_id = user_model.insert_user(new_user)
        created_user = user_model.get_user_from_id(new_user_id)
    except Exception as e:
        return "Exception...", 404

    return jsonify(created_user)

def login(request):
    credential = request.json
    user_model = UserModel()
    email = credential['email']
    password = credential['password']

    row = user_model.get_user_from_email(email)

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


def upload_profile_picture(request):
    if 'profile_pic' not in request.files:
        return 'File is Missing...', 404

    img = request.files['profile_pic']
    if img.filename =='':
        return 'File is Missing...', 404

    user_id = g.user_id

    # save image files
    filename = secure_filename(img.filename)
    upload_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    img.save(upload_file_path)

    # update to db
    user_model = UserModel()
    user_model.insert_profile_picture(upload_file_path, user_id)
    return '', 200


def get_profile_picture(request, user_id):
    return '', 200
    # try:
    #     user_model = UserModel()
    #     profile_picture_path = user_model.get_profile_picture_path(user_id)
    #     s3_connection = s3.s3_connection(current_app)
    # if profile_picture_path:
    #     return send_file(profile_picture_path)
    # else:
    #     return '', 404


