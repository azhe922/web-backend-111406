from mongoengine import EmbeddedDocument, StringField, ListField, BooleanField
import json
from datetime import datetime
from app.utils.backend_util import datetime_strf_YYYYmmdd


class UserTodo(EmbeddedDocument):
    """    
    user_todo-紀錄每周排定日期的訓練計劃

    |   欄位名稱   |     意義     | 資料型態 | 預設值 |
    |:------------:|:------------:|:--------:|:------:|
    | target_times |   目標次數   |  array   |        |
    | target_date  | 目標完成時間 |  string  |        |
    |   complete   |   完成與否   | boolean  | False  |
    | actual_times |   實際次數   |  array  |        |
    """
    target_times = ListField(required=True, default=[
        {"times": 15, "set": 2, "total": 30, "part": 0},
        {"times": 8, "set": 1, "total": 8, "part": 1},
        {"times": 15, "set": 2, "total": 30, "part": 2}
    ])
    target_date = StringField(required=True)
    complete = BooleanField(default=False)
    actual_times = ListField(default=[{
        'part': 0,
        'hand': 'left',
        'times': 0,
    }, {
        'part': 0,
        'hand': 'right',
        'times': 0,
    }, {
        'part': 1,
        'hand': 'left',
        'times': 0,
    }, {
        'part': 1,
        'hand': 'right',
        'times': 0,
    }, {
        'part': 2,
        'times': 0
    }], max_length=5)

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        target_date = datetime.strptime(self.target_date, '%Y%m%d').timestamp()
        result['target_date'] = datetime_strf_YYYYmmdd(target_date)
        return result
