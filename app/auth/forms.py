from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z}[A-Za-z0-9_]*$', 0,
                                                                                         '只能输入字母、数字和下划线')])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 64), EqualTo('password2', '密码不一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=field.data).first():
            raise ValidationError('邮箱已注册！')

    def validate_username(self, field):
        if User.objects(username=field.data).first():
            raise ValidationError('用户名已注册！')