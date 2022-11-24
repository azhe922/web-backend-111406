from flask import make_response
from flask_login import login_required
from flasgger import swag_from
import logging
from http import HTTPStatus
from . import api
from app.service.record_service import search_records_by_userid, get_count, get_biceps_means, get_quadriceps_means
from app.utils.backend_error import BackendException
from app.api.api_doc import record_search as search_doc, record_count as count_doc
from app.utils.backend_decorator import role_check
from app.enums.user_role import UserRole

root_path = "/record"
logger = logging.getLogger(__name__)

# 查詢使用者所有測試紀錄


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(search_doc)
def search_record(user_id):
    """查詢使用者所有測試紀錄
    """
    try:
        result = search_records_by_userid(user_id)
        message = "查詢成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 查詢使用者測試筆數


@api.route(f"{root_path}/count/<user_id>", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(count_doc)
def get_record_count(user_id):
    """查詢使用者測試筆數
    """
    try:
        result = get_count(user_id)
        message = "查詢使用者測試筆數成功"
        logger.info(message)
        return make_response({"message": message, "count": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)
    
# 查詢二頭肌統計平均數
    
@api.route(f"{root_path}/biceps/means", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
def biceps_means():
    """查詢上肢統計平均數
    """
    try:
        result = get_biceps_means()
        message = "查詢上肢統計平均數成功"
        logger.info(message)
        return make_response({"message": message, "means": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 查詢股四頭肌統計平均數

@api.route(f"{root_path}/quadriceps/means", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
def quadriceps_means():
    """查詢下肢統計平均數
    """
    try:
        result = get_quadriceps_means()
        message = "查詢下肢統計平均數成功"
        logger.info(message)
        return make_response({"message": message, "means": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)