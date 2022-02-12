from flask import Blueprint

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route('/ping', methods=['GET'])
def hello_world():
    return 'pong'

@bp.route('/', methods=['GET'])
def hello_world():
    return 'Hello, This is Miniter WAS Server'

@bp.route('/health', methods=['GET'])
def hello_world():
    return '', 200