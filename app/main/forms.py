from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from ..models import Permission


class EditProfileForm(FlaskForm):
    about_me = StringField('about me')
    submit = SubmitField('submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username')
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', choices=[(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, 'User'),
                                        (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES |
                                         Permission.MODERATE_COMMENTS, 'Moderator'),
                                        (Permission.ADMINISTER, 'Administrator')], coerce=int)
    about_me = TextAreaField('About me')
    submit = SubmitField()
