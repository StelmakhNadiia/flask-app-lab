"""Insert data into products table

Revision ID: cbb828587d0c
Revises: e48bdef74d2b
Create Date: 2025-11-21 02:05:43.390040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float, Boolean

# revision identifiers, used by Alembic.
revision = 'cbb828587d0c'
down_revision = 'e48bdef74d2b'
branch_labels = None
depends_on = None


def upgrade():
    # --- Описи таблиць для bulk_insert ---
    categories_table = table('categories', column('id', sa.Integer), column('name', sa.String))

    products_table = table('products',
        column('name', sa.String),
        column('price', sa.Float),
        column('active', sa.Boolean),
        column('category_id', sa.Integer),
    )

    # --- Вставка категорій ---
    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    # --- Вставка продуктів ---
    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone LG', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])

def downgrade():
   # Видаляємо тільки ці вставлені продукти та категорії

   # Видаляємо продукти по назвах
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Ultrabook', 'Laptop', 'Smartphone LG', 'Novel', 'T-Shirt');
    """)

    # Видаляємо категорії по назвах
    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)