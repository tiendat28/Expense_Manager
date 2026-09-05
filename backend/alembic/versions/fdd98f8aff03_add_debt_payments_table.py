"""add debt payments table

Revision ID: fdd98f8aff03
Revises: 0001
Create Date: 2026-09-04 15:18:52.211954

"""
from alembic import op
import sqlalchemy as sa


revision = 'fdd98f8aff03'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('debt_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('debt_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=14, scale=2), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['debt_id'], ['debts.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_debt_payments_debt_id'), 'debt_payments', ['debt_id'], unique=False)
    op.create_index(op.f('ix_debt_payments_id'), 'debt_payments', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_debt_payments_id'), table_name='debt_payments')
    op.drop_index(op.f('ix_debt_payments_debt_id'), table_name='debt_payments')
    op.drop_table('debt_payments')
