from flask import request, make_response, session
from flask_login import login_required, logout_user
from flasgger import swag_from
from http import HTTPStatus
import logging
from werkzeug.datastructures import ImmutableMultiDict
from app.service.user_service import user_signup_service, search_user_service, getuser_by_id_service, user_login_service, update_user_service, update_pwd_service
from . import api
from app.utils.backend_error import LoginFailedException, BackendException, UserIdOrEmailAlreadyExistedException, NotFoundUseridException, PasswordIncorrectException
from app.api.api_doc import user_signup as signup_doc, user_login as login_doc, user_search as search_doc, user_get as get_doc, user_logout as logout_doc
from app.form.user_form import UserForm
from app.utils.backend_decorator import role_check
from app.enums.user_role import UserRole

root_path = "/user"
logger = logging.getLogger(__name__)

# 使用者註冊


@api.route(f"{root_path}/signup", methods=['POST'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(signup_doc)
def signup():
    """使用者註冊
    """
    data = request.get_json()
    logger.info(f"{data['user_id']} 使用者註冊: {data}")
    try:
        user_signup_service(data)
        message = "註冊成功"
        logger.info(f"{data['user_id']} {message}")
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case UserIdOrEmailAlreadyExistedException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 使用者登入


@api.route(f"{root_path}/login", methods=['POST'])
@swag_from(login_doc)
def login():
    """使用者登入    
    """
    form_input = ImmutableMultiDict(request.get_json())
    form = UserForm(form_input)
    try:
        user_login_service(form)
        message = "登入成功"
        logger.info(f"{form.user_id.data} {message}")
        session.permanent = True
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case LoginFailedException.__name__ | NotFoundUseridException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 查詢所有使用者


@api.route(root_path, methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(search_doc)
def search_user():
    """查詢所有使用者
    需要管理者帳號才能使用
    """
    try:
        result = search_user_service()
        message = "查詢成功"
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        e.with_traceback()
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 依ID查詢使用者


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@login_required
@role_check(role=UserRole.manager.value)
@swag_from(get_doc)
def getuser_by_id(user_id):
    """依使用者ID查詢用戶資料
    """
    try:
        result = getuser_by_id_service(user_id)
        message = "查詢成功"
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 使用者資料更新


@api.route(f"{root_path}/update/<user_id>", methods=['POST'])
@login_required
@role_check(role=UserRole.manager.value)
def update_user(user_id):
    data = request.get_json()
    logger.info(f"{user_id} 使用者資料更新: {data}")
    try:
        update_user_service(data, user_id)
        message = "更新成功"
        logger.info(f"{user_id} {message}")
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 修改密碼


# @api.route(f"{root_path}/update/password/<user_id>", methods=['POST'])
# @login_required
# def update_pwd(user_id):
#     data = request.get_json()
#     logger.info(f"{user_id} 修改密碼")
#     try:
#         update_pwd_service(data, user_id)
#         message = "更新成功"
#         logger.info(message)
#         return make_response({"message": message}, HTTPStatus.OK)
#     except Exception as e:
#         match e.__class__.__name__:
#             case PasswordIncorrectException.__name__:
#                 pass
#             case _:
#                 logger.error(str(e))
#                 e = BackendException()
#         (message, status) = e.get_response_message()
#         return make_response({"message": message}, status)


@api.route(f"{root_path}/logout", methods=['GET'])
@login_required
@swag_from(logout_doc)
def logout():
    """使用者登出    
    """
    try:
        message = "登出成功"
        logout_user()
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)