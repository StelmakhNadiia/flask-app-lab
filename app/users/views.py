# app/users/views.py
import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, url_for, flash, make_response, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.users.models import User
# Зверніть увагу на крапку перед forms - це імпорт з папки users
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm 
from datetime import datetime, timezone

users_bp = Blueprint('users_bp', __name__, template_folder='templates', url_prefix='/users')

@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

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
            login_user(user, remember=form.remember.data)
            flash('Ви успішно увійшли!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users_bp.account'))
        else:
            flash('Неправильний логін або пароль.', 'danger')

    return render_template('users/login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users_bp.login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Шлях до папки images, як ви просили
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users_bp.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='images/' + current_user.image)
    return render_template('users/account.html', image_file=image_file, form=form)

@users_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Ваш пароль успішно оновлено!', 'success')
            return redirect(url_for('users_bp.account'))
        else:
            flash('Невірний поточний пароль.', 'danger')
    return render_template('users/change_password.html', form=form)

@users_bp.route('/set-profile-theme/<theme>')
def set_profile_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'dark'
    
    response = make_response(redirect(request.referrer or url_for('users_bp.account')))
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

@users_bp.route('/all')
@login_required
def all_users():
    users = db.session.scalars(db.select(User)).all()
    count = len(users)
    return render_template('users/all_users.html', users=users, count=count)