from flask import Blueprint, request
from services import service_user
from .common import login_required

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/sign-up", methods=['POST'])
def sign_up():
    """
    회원가입 API
    :return: 생성된 유저 정보
    """
    return service_user.sign_up(request)



@bp.route('/login', methods=['POST'])
def login():
    return service_user.login(request)



@bp.route('/profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    return service_user.upload_profile_picture(request)


@bp.route('/profile-picture/<int:user_id>', methods=['GET'])
def get_profile_picture(user_id):
    return service_user.get_profile_picture(request, user_id)
