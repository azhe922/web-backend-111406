from app.model.target import Target
from app.utils.backend_util import get_week, dict_to_json
from app.utils.rsa_util import encrypt
from app.model.user_loginrecord import UserLoginRecord
from app.model.default_target import DefaultTarget
from datetime import datetime


def get_target_service(user_id, search_mode: str | None):
    if search_mode == 'current':    
        now = datetime.now()
        today = now.strftime('%Y%m%d')
        target = Target.objects.get(user_id=user_id, end_date__gt=today)
        user_todos = target.user_todos
        return [user_todo.to_json() for user_todo in user_todos]
    else:
        targets = Target.objects(user_id=user_id)
        return [target.to_json() for target in targets]

def get_newmission_tokens_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    if targets:
        tokens = []
        user_ids = []
        [__add_todo_is_notcomplete([today], target, user_ids) for target in targets]
        __get_tokens(user_ids, tokens)
        return __convert_to_bytes_and_encrypt(tokens).decode()

def get_notcomplete_tokens_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    if targets:
        tokens = []
        user_ids = []
        this_week_days = [d.strftime('%Y%m%d') for d in get_week(now) if d < now]
        [__add_todo_is_notcomplete(this_week_days, target, user_ids) for target in targets]
        __get_tokens(user_ids, tokens)
        return __convert_to_bytes_and_encrypt(tokens).decode()

def search_userids_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    return sorted(list({target.user_id for target in Target.objects(end_date__gt=today).only('user_id')}))

def update_target_times_service(user_id, target_date, data):
    target = __get_target_from_today(user_id).get()
    if data['mode'] == 'selected':
        should_be_updated_todo = target.user_todos.filter(target_date=target_date).get()
        should_be_updated_todo.target_times = data['target_times']        
    elif data['mode'] == 'after':
        user_todos = target.user_todos
        should_be_updated_todo = [user_todo for user_todo in user_todos if user_todo.target_date >= target_date]
        for todo in should_be_updated_todo:
            todo.target_times = data['target_times']
        __update_default_target(user_id, data)
    target.save()

def __update_default_target(user_id, data):
    default_target = DefaultTarget.objects(user_id=user_id)
    if default_target:
        default_target = default_target.get()
        default_target.target_times = data['target_times']
        default_target.valid = True
        default_target.save()
    else:
        DefaultTarget(user_id=user_id, target_times=data['target_times']).save()

def __get_tokens(user_ids, tokens):
    for user_id in user_ids:
        loginrecord = UserLoginRecord.objects(user_id=user_id).get()
        if loginrecord.registration_token:
            tokens.append(loginrecord.registration_token)

def __convert_to_bytes_and_encrypt(user_ids):
    user_ids_bytes = dict_to_json(user_ids).encode('utf-8')
    return encrypt(user_ids_bytes)

def __add_todo_is_notcomplete(check_days: list, target, result):
    for day in check_days:
        user_todos = target.user_todos.filter(target_date=day)
        if user_todos and not user_todos.get().complete:
            result.append(target.user_id)
            return

def __get_target_from_today(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    return Target.objects(user_id=user_id, end_date__gt=today)