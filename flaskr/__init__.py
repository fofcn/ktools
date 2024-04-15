
from flask import Blueprint, Flask
from . import config

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(config.FlaskConfig)

    from . import index
    app.register_blueprint(index.indexbp)

    return app