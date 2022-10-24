from flask_wtf import FlaskForm
from wtforms.fields import StringField

class UserForm(FlaskForm):
    user_id = StringField()
    password = StringField()
