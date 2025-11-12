from flask import Blueprint

# 1. Визначення об'єкта Blueprint (ім'я об'єкта post_bp)
post_bp = Blueprint(
    'posts', # Ім'я блюпринта для url_for
    __name__,
    template_folder='templates/posts',
    static_folder='static'
)

# 2. Імпорт views в кінці, щоб запобігти циклічному імпорту.
# Тут ми імпортуємо view-функції, які використовують об'єкт post_bp
from . import views