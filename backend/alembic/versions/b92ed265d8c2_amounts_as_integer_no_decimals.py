"""amounts as integer, no decimals

Revision ID: b92ed265d8c2
Revises: 2638e190acbf
Create Date: 2026-09-04 17:12:56.330242

"""
from alembic import op
import sqlalchemy as sa


revision = 'b92ed265d8c2'
down_revision = '2638e190acbf'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('category_budgets', 'limit_amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('debt_payments', 'amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('debts', 'total_amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('debts', 'paid_amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=True,
               existing_server_default=sa.text("'0'::numeric"))
    op.alter_column('recurring_bills', 'amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('savings_contributions', 'amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('savings_goals', 'target_amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('transactions', 'amount',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    op.alter_column('users', 'monthly_budget',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=True,
               existing_server_default=sa.text("'5000000'::numeric"))


def downgrade():
    op.alter_column('users', 'monthly_budget',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=True,
               existing_server_default=sa.text("'5000000'::numeric"))
    op.alter_column('transactions', 'amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('savings_goals', 'target_amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('savings_contributions', 'amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('recurring_bills', 'amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('debts', 'paid_amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=True,
               existing_server_default=sa.text("'0'::numeric"))
    op.alter_column('debts', 'total_amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('debt_payments', 'amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
    op.alter_column('category_budgets', 'limit_amount',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.NUMERIC(precision=14, scale=2),
               existing_nullable=False)
