from app.model.logrecord import LogRecord
from app.utils.backend_util import datetime_YYYYmmdd_to_timestamp


def search_log_service(start_time, end_time, user_id):
    start_time = datetime_YYYYmmdd_to_timestamp(start_time) if start_time else 0.0
    end_time = datetime_YYYYmmdd_to_timestamp(end_time) if end_time else 9999999999.0
    logs = LogRecord.objects(action_time__gte=start_time, action_time__lte = end_time).order_by('-action_time')
    if user_id:
        logs = logs.filter(user_id = user_id)
    return [log.to_json() for log in logs]