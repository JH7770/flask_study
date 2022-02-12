from flask import Flask
from flask_cors import CORS
from router import blueprints


def create_app():
    app = Flask(__name__)
    CORS(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    return app

