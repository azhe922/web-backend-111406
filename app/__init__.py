from flask import Flask
from flask_cors import CORS
from app_config import config
from flasgger import Swagger

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:3000"]}})

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    Swagger(app)

    return app