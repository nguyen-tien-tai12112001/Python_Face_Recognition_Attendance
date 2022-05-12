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