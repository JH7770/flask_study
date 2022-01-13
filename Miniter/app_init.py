from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

from router import blueprints


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


def create_app(test_config=None):
    app = Flask(__name__)

    # regist config
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    # database connect
    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    # set Custom JSON Encoder
    app.json_encoder = CustomJSONEncoder

    # set blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
