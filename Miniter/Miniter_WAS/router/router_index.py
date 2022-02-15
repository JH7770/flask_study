from flask import Blueprint

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route('/ping', methods=['GET'])
def hello_world():
    return 'pong'

@bp.route('/', methods=['GET'])
def index():
    return 'Hello, This is Miniter WAS Server'

