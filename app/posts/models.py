from datetime import datetime
from .. import db
import enum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey, Integer, String # Додані Integer, String

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.users.models import User

# === 1. Асоціативна таблиця (Крок 9) ===
# Вона створюється як об'єкт db.Table, а не клас.
# Важливо: повинна бути оголошена ПЕРЕД класами Post та Tag.
post_tags = db.Table(
    'post_tags',
    db.Model.metadata,
    db.Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# === 2. Модель Tag (Крок 9) ===
class Tag(db.Model):
    __tablename__ = 'tags'

    id: Mapped[int] = db.mapped_column(primary_key=True)
    name: Mapped[str] = db.mapped_column(String(50), unique=True, nullable=False)

    # Зв'язок з постами (secondary вказує на проміжну таблицю post_tags)
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other  = 'other'

class Post(db.Model):
    """
    ORM-модель Post, оновлена до стилю Flask-SQLAlchemy 2.0+.
    """
    __tablename__ = 'posts'
    
    id: Mapped[int] = db.mapped_column(primary_key=True)
    
    title: Mapped[str] = db.mapped_column(
        db.String(150), nullable=False
    )
    
    content: Mapped[str] = db.mapped_column(
        db.Text, nullable=False
    )
    
    posted: Mapped[datetime] = db.mapped_column(
        default=datetime.utcnow
    )
    
    category: Mapped[PostCategory] = db.mapped_column(
        db.Enum(PostCategory)
    )
    
    is_active: Mapped[bool] = db.mapped_column(
        default=True
    )
    
    # === Зв'язок з User ===
    user_id: Mapped[int] = db.mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    # === 3. Зв'язок з Tag (Крок 9) ===
    # secondary=post_tags обов'язковий для Many-to-Many
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags, back_populates="posts"
    )

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"