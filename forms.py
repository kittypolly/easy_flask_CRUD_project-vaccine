from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class Patient_addform(FlaskForm):

    Patient_add = StringField('추가할 환자정보를 입력해주세요:')
    submit = SubmitField('환자정보를 추가합니다.')

class Patient_delform(FlaskForm):

    Patient_del = IntegerField('제거할 환자아이디를 입력해주세요')
    submit = SubmitField('해당 환자데이터를 제거합니다.')

class Vaccine_addform(FlaskForm):

    Vaccine_add = StringField('추가할 백신이름을 입력해주세요:')
    Patient_id = IntegerField('백신을 추가할 환자아이디를 입력해주세요.')
    submit = SubmitField('백신을 해당 아이디에 추가합니다.')