"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-04

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("monthly_budget", sa.Numeric(14, 2), server_default="5000000"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("category", sa.String, nullable=False),
        sa.Column("note", sa.String, server_default=""),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("type", sa.Enum("expense", "income", name="transactiontype"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "savings_goals",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("icon", sa.String, server_default="🎯"),
        sa.Column("target_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "savings_contributions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("goal_id", sa.Integer, sa.ForeignKey("savings_goals.id"), nullable=False, index=True),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "debts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("person_name", sa.String, nullable=False),
        sa.Column("type", sa.Enum("owe", "lent", name="debttype"), nullable=False),
        sa.Column("total_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("paid_amount", sa.Numeric(14, 2), server_default="0"),
        sa.Column("due_date", sa.Date, nullable=True),
        sa.Column("note", sa.String, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "recurring_bills",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("category", sa.String, server_default="Hóa đơn"),
        sa.Column("due_day", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.true()),
        sa.Column("last_paid_month", sa.String, nullable=True),
    )

    op.create_table(
        "category_budgets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("category", sa.String, nullable=False),
        sa.Column("limit_amount", sa.Numeric(14, 2), nullable=False),
        sa.UniqueConstraint("user_id", "category", name="uq_user_category"),
    )


def downgrade():
    op.drop_table("category_budgets")
    op.drop_table("recurring_bills")
    op.drop_table("debts")
    op.drop_table("savings_contributions")
    op.drop_table("savings_goals")
    op.drop_table("transactions")
    op.drop_table("users")
    sa.Enum(name="transactiontype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="debttype").drop(op.get_bind(), checkfirst=True)
