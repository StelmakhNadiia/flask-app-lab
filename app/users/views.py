# app/users/views.py
from flask import render_template, request, redirect, url_for, flash, make_response, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.users.models import User
from .forms import LoginForm, RegistrationForm

users_bp = Blueprint('users_bp', __name__, template_folder='templates', url_prefix='/users')


@users_bp.route('/')
@login_required
def users_list():
    users = db.session.scalars(db.select(User)).all()
    count = len(users)
    return render_template('users/users.html', users=users, count=count)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Акаунт створено для {form.username.data}! Тепер ви можете увійти.', 'success')
        return redirect(url_for('users_bp.login'))
    
    return render_template('users/register.html', form=form)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.account'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data) # Flask-Login записує сесію
            flash('Ви успішно увійшли!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users_bp.account'))
        else:
            flash('Неправильний логін або пароль.', 'danger')

    return render_template('users/login.html', form=form)

@users_bp.route('/logout')
@login_required # Додаємо захист, щоб вийти міг тільки той, хто увійшов
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users_bp.login'))

@users_bp.route('/account')
@login_required # Захищаємо сторінку акаунта
def account():
    return render_template('users/account.html')


@users_bp.route('/set-profile-theme/<theme>')
def set_profile_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'dark'
    
    response = make_response(redirect(request.referrer or url_for('users_bp.account')))
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

@users_bp.route('/all')
@login_required  # Захищаємо маршрут: тільки для авторизованих
def all_users():
    # Отримуємо всіх користувачів з БД (синтаксис SQLAlchemy 2.0)
    users = db.session.scalars(db.select(User)).all()
    
    # Рахуємо кількість
    count = len(users)
    
    return render_template('users/all_users.html', users=users, count=count)