from app.model.target import Target
from app.utils.backend_util import get_week, dict_to_json
from app.utils.rsa_util import encrypt
from datetime import datetime


def get_target_service(user_id):
    targets = Target.objects(user_id=user_id)
    return [target.to_json() for target in targets]

def get_newmission_user_ids_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    user_ids = []
    if targets:
        [__add_todo_is_notcomplete([today], target, user_ids) for target in targets]
        return __convert_to_bytes_and_encrypt(user_ids).decode()

def get_notcomplete_user_ids_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    user_ids = []
    if targets:
        this_week_days = [d.strftime('%Y%m%d') for d in get_week(now) if d < now]
        [__add_todo_is_notcomplete(this_week_days, target, user_ids) for target in targets]
        return __convert_to_bytes_and_encrypt(user_ids).decode()

def __convert_to_bytes_and_encrypt(user_ids):
    user_ids_bytes = dict_to_json(user_ids).encode('utf-8')
    return encrypt(user_ids_bytes)

def __add_todo_is_notcomplete(check_days: list, target, result):
    for day in check_days:
        user_todos = target.user_todos.filter(target_date=day)
        if user_todos and not user_todos.get().complete:
            result.append(target.user_id)
            return
