from flask import Flask
from flask_cors import CORS
from app_config import config
from flasgger import Swagger
from flask_login import LoginManager
from mongoengine import connect


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:3000",
         "http://localhost:3000", "https://frontend-111406.onrender.com"]}}, supports_credentials=True)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    Swagger(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    connect(host=app.config["DB_HOST"])

    from app.model.user import User

    @login_manager.user_loader
    def load_user(id):
        # since the id is just the primary key of our user table, use it in the query for the user
        return User.objects.get(id=id)

    return app
