from flask import Blueprint

# Додаємо static_folder='static'
disciplines_bp = Blueprint('disciplines_bp', __name__, 
                           template_folder='templates',
                           static_folder='static', 
                           static_url_path='/disciplines/static')

from . import views