from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey
# from app.users.models import User # Цей імпорт може створити циклічне посилання, тому використовуємо рядок "User"

class DisciplineCategory(db.Model):

    __tablename__ = "discipline_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    # Зв'язок
    disciplines: Mapped[list["Discipline"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<DisciplineCategory '{self.name}'>"

class Discipline(db.Model):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    category_id: Mapped[int] = mapped_column(ForeignKey("discipline_categories.id"), nullable=False)
   
    category: Mapped["DisciplineCategory"] = relationship(back_populates="disciplines")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship()

    def __repr__(self):
        return f"<Discipline '{self.name}'>"