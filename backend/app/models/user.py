from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    monthly_budget = Column(Numeric(14, 0), default=5000000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    savings_goals = relationship("SavingsGoal", back_populates="user", cascade="all, delete-orphan")
    debts = relationship("DebtRecord", back_populates="user", cascade="all, delete-orphan")
    bills = relationship("RecurringBill", back_populates="user", cascade="all, delete-orphan")
    category_budgets = relationship("CategoryBudget", back_populates="user", cascade="all, delete-orphan")
    gift_money_records = relationship("GiftMoneyRecord", back_populates="user", cascade="all, delete-orphan")
