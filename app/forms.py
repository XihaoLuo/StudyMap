from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms import TextAreaField, validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Building, StudySpace, User, Post

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CheckinForm(FlaskForm):
    def get_spaces():
        spaces = StudySpace.query.all();
        choices = []
        for space in spaces:
            choices.append((space.id, (space.building.name + ': ' + space.name) ))
        return choices

    post_body = TextAreaField('Post text', validators=[validators.optional(), Length(min=0, max=140)])
    space_id = SelectField('Select space', choices=get_spaces(), coerce=int, validators=[validators.optional()])
    submit = SubmitField('Post')
