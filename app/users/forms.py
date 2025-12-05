# app/users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.users.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Це поле обов'язкове.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів.")
    ])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Ім'я користувача має бути від 4 до 14 символів."),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
               'Username must have only letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Пароль має бути не менше 6 символів.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Паролі повинні співпадати.')
    ])
    submit = SubmitField('Sign Up')

    # Валідація на унікальність (запити до БД)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Таке ім\'я користувача вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такий email вже зареєстрований. Будь ласка, увійдіть.')