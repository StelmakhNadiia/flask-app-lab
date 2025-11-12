from . import post_bp
from flask import render_template, redirect, url_for, flash, abort, request, session
from app import db 
from .models import Post 
from .forms import PostForm 
from datetime import datetime




def get_current_author():
    # Використовує session
    return session.get('username', 'Anonymous')

# 1. READ (Список постів)
@post_bp.route('/') 
def get_posts():
    """
    Відображає список лише АКТИВНИХ постів,
    сортуючи їх за датою (новіші зверху).
    """
    posts = db.session.scalars(
        db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    ).all()
    
    return render_template("posts.html", posts=posts)

# 2. READ (Деталі одного поста)
@post_bp.route('/<int:id>') 
def detail_post(id):
    """
    Відображає деталі одного поста.
    Якщо пост неактивний, показує 404.
    """
    post = db.get_or_404(Post, id)
    
    if not post.is_active:
        abort(404) # Показуємо сторінку "Не знайдено"
        
    return render_template("detail_post.html", post=post)

# 3. CREATE (Створення нового поста)
@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    """
    Обробляє створення нового поста.
    """
    form = PostForm()
    if form.validate_on_submit():
        # Створюємо новий екземпляр Post з даних форми
        new_post = Post(
            title=form.title.data,
            content=form.content.data,     # Використовуємо 'content'
            posted=form.publish_date.data, # ВИПРАВЛЕНО: Використовуємо 'publish_date' з форми
            is_active=form.is_active.data,
            category=form.category.data,
            author=get_current_author()
        )
        db.session.add(new_post)
        db.session.commit()
        
        flash(f'Пост "{new_post.title}" успішно створено!', 'success')
        return redirect(url_for('posts.detail_post', id=new_post.id))
    
    # Якщо GET-запит, просто показуємо форму
    return render_template("add_post.html", form=form, form_title="Створення нового поста")

# 4. UPDATE (Редагування поста)
@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    """
    Обробляє редагування існуючого поста.
    """
    post = db.get_or_404(Post, id)
    
    # 'obj=post' автоматично заповнить поля форми
    # даними з поста, який ми редагуємо.
    form = PostForm(obj=post) 

    if request.method == 'GET':
        # Це потрібно, якщо ви використовуєте ручне заповнення (як у вашому коді)
        # Якщо ви використовуєте PostForm(obj=post), Flask-WTF може автоматично
        # заповнити відповідні поля, але post.posted і form.publish_date не збігаються.
        form.publish_date.data = post.posted # ВИПРАВЛЕНО: Ручна ініціалізація
    
    if form.validate_on_submit():
        # Оновлюємо поля існуючого 'post'
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.author = form.author.data
        
        db.session.commit() # Зберігаємо зміни
        
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    # Якщо GET-запит, показуємо форму, заповнену даними
    return render_template("add_post.html", form=form, form_title="Редагування поста")

# 5. DELETE (Видалення поста)
@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    """
    Обробляє видалення поста.
    """
    post = db.get_or_404(Post, id)

    form = PostForm() 
    
    if request.method == 'POST':
        if form.validate_on_submit(): 
            db.session.delete(post)
        db.session.commit()
        flash('Пост успішно видалено.', 'success')
        return redirect(url_for('posts.get_posts'))
    else: flash('Помилка безпеки. Спробуйте ще раз.', 'danger')

    
    # Якщо GET-запит, показуємо сторінку підтвердження
    return render_template("delete_confirm.html", post=post, form=form)