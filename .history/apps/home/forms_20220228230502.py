from importlib_metadata import email
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, FileField, DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Email, DataRequired

class CreateStudent(FlaskForm):
    msv = TextField('MSV',
                         id='msv_create',
                         validators=[DataRequired()])
    name = TextField('Name',
                      id='name_create',
                      validators=[DataRequired()])
    phone = TextField('Phone',
                             id='phone_create',
                             validators=[DataRequired()])
    email = TextField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    DOBs = DateField('Date', format='%Y-%m-%d',
                     id='date_create',
                    validators=[DataRequired()])
    classes = SelectField('Classes',
                             id='class_create',
                             choices=[('TT', 'TT'), 
                             ('TA', 'TA'),
                             ('TS', 'TS'),
                             ('TI', 'TI'),
                             ('QT', 'QT'),
                             ],
                             default='TT')
                             
    img = TextField('Photo',
                         id='photo_create',
                         validators=[DataRequired()])
class CreateClass(FlaskForm):
    note = TextField('Note',
                         id='note_create',
                         validators=[DataRequired()])
    name = TextField('Name',
                      id='name_create',
                      validators=[DataRequired()])
class CreateSchedule(FlaskForm):
    startDate = TextField('StartDate',
                         id='start_create',
                         validators=[DataRequired()])
    endDate = TextField('EndDate',
                      id='endate_create',
                      validators=[DataRequired()])
class CreateTeacher(FlaskForm):
    mgv = TextField('MGV',
                         id='mgv_create',
                         validators=[DataRequired()])
    fullname = TextField('FullName',
                      id='fullname_create',
                      validators=[DataRequired()])
    gender = TextField('Gender',
                      id='gender_create',
                      validators=[DataRequired()])