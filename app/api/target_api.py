from flask import make_response, request
from flask_login import login_required
from flasgger import swag_from
import logging
from http import HTTPStatus
from app.service.target_service import get_target_service, get_newmission_tokens_service, get_notcomplete_tokens_service, search_userids_service, update_target_times_service
from app.utils.backend_error import BackendException
from . import api
from app.api.api_doc import target_get as get_doc
from app.utils.backend_decorator import role_check, fcm_check
from app.enums.user_role import UserRole
from app.utils.backend_util import datetime_YYYY_mm_dd_to_YYYYmmdd

root_path = "/target"
logger = logging.getLogger(__name__)

# # 新增個人計劃表


# @api.route(root_path, methods=['POST'])
# def add_target():
#     data = request.get_json()
#     message = ""
#     status = 200
#     try:
#         add_target_service(data)
#         message = "新增訓練計劃表成功"
#         logger.info(message)
#     except Exception as e:
#         match e.__class__.__name__:
#             case _:
#                 logger.error(str(e))
#                 e = BackendException()
#         (message, status) = e.get_response_message()
#     response = make_response({"message": message}, status)
#     return response

# 查詢個人計劃表


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(get_doc)
def get_target(user_id):
    """查詢個人計劃表
    """
    try:
        mode = request.args.get("mode")
        result = get_target_service(user_id, mode)
        message = "查詢訓練計劃表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)


@api.route(f"{root_path}/get/newmission", methods=['GET'])
@fcm_check
def get_newmission_token():
    """查詢今日有新任務之使用者token
    """
    try:
        result = get_newmission_tokens_service()
        message = "查詢今日有新任務之使用者token成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)


@api.route(f"{root_path}/get/notcomplete", methods=['GET'])
@fcm_check
def get_notcomplete_token():
    """查詢有未完成任務之使用者token
    """
    try:
        result = get_notcomplete_tokens_service()
        message = "查詢有未完成任務之使用者token成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 查詢既有訓練表之名單


@api.route(f"{root_path}/search/user_ids", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
def search_userids():
    """查詢既有訓練表之名單
    """
    try:
        result = search_userids_service()
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

# 更新計畫表


@api.route(f"{root_path}/update/<user_id>/<target_date>", methods=['POST'])
@login_required
@role_check(role=UserRole.manager.value)
def update_target_times(user_id, target_date):
    data = request.get_json()
    try:
        target_date = datetime_YYYY_mm_dd_to_YYYYmmdd(target_date)
        result = update_target_times_service(user_id, target_date, data)
        message = "更新訓練計劃表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)