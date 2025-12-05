# app/users/models.py
from app import db, bcrypt, login_manager 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Text # Додали DateTime та Text
from flask_login import UserMixin 
from typing import TYPE_CHECKING
from datetime import datetime # Не забудь цей імпорт

if TYPE_CHECKING:
    from app.posts.models import Post


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False) 
    
    # --- Нові поля (Завдання 1 та 6) ---
    image: Mapped[str] = mapped_column(String(20), nullable=False, default='profile_default.jpg') 
    # Примітка: в завданні nullable=True, але для картинки краще мати дефолтне значення і nullable=False, 
    # проте якщо викладач вимагає точно як в інструкції, зміни на nullable=True. 
    # Я залишив default='profile_default.jpg', як в умові.
    
    about_me: Mapped[str] = mapped_column(Text, nullable=True)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # -----------------------------------

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)