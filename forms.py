from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email

class RegisterForm(FlaskForm):
    nickname = StringField('nickname', validators=[InputRequired(), Length(min=4, max=20)])
    userID = StringField('userID', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('password check', validators=[DataRequired()])




    

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')