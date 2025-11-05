from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):


    name = StringField('Name', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів.")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Email(message="Введіть дійсну email адресу.")
    ])

    phone = StringField('Phone', validators=[
        Regexp(r'^\+380\d{9}$', message="Формат номеру має бути +380XXXXXXXXX.")
    ])

    subject = SelectField('Subject', choices=[
        ('tech_support', 'Технічна підтримка'),
        ('billing', 'Питання по оплаті'),
        ('general', 'Загальне питання')
    ], validators=[DataRequired()])

    message = TextAreaField('Message', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів.")
    ])

    submit = SubmitField('Send')




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