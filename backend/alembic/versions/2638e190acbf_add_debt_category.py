"""add debt category

Revision ID: 2638e190acbf
Revises: fdd98f8aff03
Create Date: 2026-09-04 15:37:09.808958

"""
from alembic import op
import sqlalchemy as sa


revision = '2638e190acbf'
down_revision = 'fdd98f8aff03'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('debts', sa.Column('category', sa.String(), server_default='Khác', nullable=True))


def downgrade():
    op.drop_column('debts', 'category')
