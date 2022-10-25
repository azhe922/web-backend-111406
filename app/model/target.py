from mongoengine import Document, StringField, EmbeddedDocumentListField, IntField
import json
from datetime import datetime

from app.model.target_usertodo import UserTodo
from app.utils.backend_util import datetime_strf_YYYYmmddHHMMSS, datetime_strf_YYYYmmdd


class Target(Document):
    """
    target-運動目標

    |  欄位名稱  |             意義             | 資料型態 | 預設值 |
    |:----------:|:----------------------------:|:--------:|:------:|
    |     id     |           流水編號           |  string  |        |
    |  user_id   |          使用者帳號          |  string  |        |
    | start_date |         訓練開始時間         |  string  |        |
    |  end_date  |         訓練結束時間         |  string  |        |
    | user_todos  | 使用者在特定日期該達成的目標 |  array   |        |
    """
    user_id = StringField(required=True, max_length=20)
    start_date = StringField(required=True)
    end_date = StringField(required=True)
    user_todos = EmbeddedDocumentListField(UserTodo)
    create_time = IntField()

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result['create_time'] = datetime_strf_YYYYmmddHHMMSS(self.create_time)
        start_date = datetime.strptime(self.start_date, '%Y%m%d').timestamp()
        end_date = datetime.strptime(self.end_date, '%Y%m%d').timestamp()
        result['start_date'] = datetime_strf_YYYYmmdd(start_date)
        result['end_date'] = datetime_strf_YYYYmmdd(end_date)
        return result
