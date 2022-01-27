from flask import Blueprint

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route('/ping', methods=['GET'])
def hello_world():
    return 'pong'
