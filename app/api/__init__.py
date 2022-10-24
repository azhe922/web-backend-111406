from flask import Blueprint

api = Blueprint('api', __name__)

from . import target_api, log_api, record_api, user_api

