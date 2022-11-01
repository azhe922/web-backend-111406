from mongoengine import Document, StringField, EmailField, FloatField, IntField, EnumField
from flask_login import UserMixin
from datetime import datetime
from app.enums.user_role import UserRole
from app.enums.gender import Gender
import json
from app.utils.backend_util import datetime_strf_YYYYmmddHHMMSS, datetime_YYYYmmdd_to_YYYY_mm_dd


class User(UserMixin, Document):
    """
    user-使用者資料
    |   欄位名稱   |       意義       | 資料型態 |
    |:------------:|:----------------:|:--------:|
    |      id      |     流水編號     |  string  |
    |   user_id    |    使用者帳號    |  string  |
    |   birthday   | 出生年月日(西元) |  string  |
    |    email     |       信箱       |  string  |
    |    gender    |       性別       |   int    |
    |    height    |       身高       |  float   |
    |    weight    |       體重       |  float   |
    |     role     |       權限       |   int    |
    |   password   |    使用者密碼    |  string  |
    |     name     |       暱稱       |  string  |
    | create_time  |     建立時間     |   int    |
    | update_time  |     更新時間     |   int    |
    | eth_account  |    乙太坊帳號    |  string  |
    | eth_password |    乙太坊密碼    |  string  |
    |   eth_sum    |    乙太坊金額    |   int    |
    | institution  |    單位/機構     |  string  |
    | other_detail |     其他事項     |  string  |
    """
    user_id = StringField(required=True, max_length=20)
    name = StringField(max_length=10)
    password = StringField(max_length=100)
    email = EmailField(required=True, max_length=100)
    height = FloatField(max_length=10)
    weight = FloatField(max_length=10)
    gender = EnumField(Gender, required=True, max_length=1)
    birthday = StringField(required=True, max_length=10)
    role = EnumField(UserRole, required=True, max_length=1)
    reference = StringField(max_length=20)
    create_time = IntField()
    update_time = IntField()
    eth_account = StringField(max_length=100)
    eth_password = StringField(max_length=100)
    eth_sum = IntField(min_value=0)
    institution = StringField()
    other_detail = StringField()
    """ {
        "isHadHypertension": boolean,
        "isHadHyperglycemia": boolean,
        "isHadHyperlipidemia": boolean,
        "isHadExerciseHabits": boolean
        }"""

    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result.pop('password', None)
        result.pop('eth_password', None)
        result.pop('eth_account', None)
        result['gender'] = self.gender.description
        result['role'] = self.role.description
        result['create_time'] = datetime_strf_YYYYmmddHHMMSS(self.create_time)
        result['birthday'] = datetime_YYYYmmdd_to_YYYY_mm_dd(self.birthday)
        return result
