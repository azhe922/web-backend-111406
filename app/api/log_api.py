from flask import make_response, request
from flask_login import login_required
from flasgger import swag_from
from http import HTTPStatus
from . import api
import logging
from app.service.log_service import search_log_service
from app.utils.backend_decorator import role_check
from app.enums.user_role import UserRole
from app.utils.backend_error import BackendException
from app.api.api_doc import log_search as search_doc

root_path = "/log"
logger = logging.getLogger(__name__)

@api.route(root_path, methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(search_doc)
def search_log():
    params = request.args
    try:
        result = search_log_service(params.get('start'), params.get('end'), params.get('userId'))
        message = "查詢Log成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        e.with_traceback()
        logger.error(str(e))
        e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)