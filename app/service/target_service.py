from app.model.target import Target
from app.utils.backend_util import get_week
from datetime import datetime


def get_target_service(user_id):
    targets = Target.objects(user_id=user_id)
    return [target.to_json() for target in targets]

def get_newmission_user_ids_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    result = []
    if targets:
        [__add_todo_is_notcomplete([today], target, result) for target in targets]
    return result

def get_notcomplete_user_ids_service():
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    targets = Target.objects(end_date__gt=today)
    result = []
    if targets:
        this_week_days = [d.strftime('%Y%m%d') for d in get_week(now) if d < now]
        [__add_todo_is_notcomplete(this_week_days, target, result) for target in targets]            
    return result

def __add_todo_is_notcomplete(check_days: list, target, result):
    for day in check_days:
        user_todos = target.user_todos.filter(target_date=day)
        if user_todos and not user_todos.get().complete:
            result.append(target.user_id)
            return
