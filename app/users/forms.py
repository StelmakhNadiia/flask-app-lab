# app/users/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from app.users.models import User
from app import db
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

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('Таке ім\'я користувача вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user:
            raise ValidationError('Такий email вже зареєстрований. Будь ласка, увійдіть.')

# --- Форма оновлення профілю ---
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Ім'я користувача має бути від 4 до 14 символів."),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
               'Username must have only letters, numbers, dots or underscores')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    
    about_me = TextAreaField('About Me', validators=[Length(max=140)])
    
    submit = SubmitField('Update')

    # Важливо: імпорт db всередині методу або зверху, якщо він там є.
    # Але тут краще використати User.query або db.session з app
    # Для уникнення циклічних імпортів, тут ми просто імпортуємо db всередині
    
    def validate_username(self, username):
        from app import db # Локальний імпорт
        if username.data != current_user.username:
            user = db.session.scalar(db.select(User).where(User.username == username.data))
            if user:
                raise ValidationError('Таке ім\'я вже зайняте. Оберіть інше.')

    def validate_email(self, email):
        from app import db # Локальний імпорт
        if email.data != current_user.email:
            user = db.session.scalar(db.select(User).where(User.email == email.data))
            if user:
                raise ValidationError('Цей email вже використовується.')

# --- Форма зміни пароля ---
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[
        DataRequired(), 
        Length(min=6, message="Пароль має бути не менше 6 символів.")
    ])
    confirm_new_password = PasswordField('Підтвердіть новий пароль', validators=[
        DataRequired(),
        EqualTo('new_password', message='Паролі повинні співпадати.')
    ])
    submit = SubmitField('Змінити пароль')