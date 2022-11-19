from flask import make_response, request, current_app as app
from functools import wraps
from flask_login import current_user
from .backend_error import AuthNotEnoughException, TokenNotProvidedException, InvalidTokenProvidedException
from .rsa_util import decrypt_token

def role_check(original_function=None, *, role=None):
    def _decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if current_user['role'].value < role:
                (message, status) = AuthNotEnoughException.get_response_body()
                return make_response({"message": message}, status)
            return function(*args, **kwargs)
        return wrapper

    # server啟動時會先將api內的裝飾器註冊一遍，沒有以下這行他會出名字重複的錯誤
    if original_function:
        _decorate.__name__ = original_function.__name__
    return _decorate

def fcm_check(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        fcm_token = request.headers.get('fcm_token')
        if not fcm_token:
            (message, status) = TokenNotProvidedException.get_response_body()
            return make_response({"message": message}, status)
        try:
            fcm_token = decrypt_token(fcm_token)
            if app.config['SECRET_KEY'] != fcm_token:
                raise InvalidTokenProvidedException()
        except Exception as e:
            (message, status) = InvalidTokenProvidedException.get_response_body()
            return make_response({"message": message}, status)
        return function(*args, **kwargs)
    return wrapper