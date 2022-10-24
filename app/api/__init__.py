from flask import Blueprint
from app.utils.backend_util import init_db, close_db

api = Blueprint('api', __name__)

from . import target_api, log_api, record_api, user_api

@api.before_request
def before_request():
    init_db()

@api.teardown_request
def teardown_request(exception):
    close_db()