import enum
from sqlalchemy import Column, Integer, String, Numeric, Date, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class TransactionType(str, enum.Enum):
    expense = "expense"
    income = "income"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(14, 0), nullable=False)
    category = Column(String, nullable=False)
    note = Column(String, default="")
    date = Column(Date, nullable=False)
    type = Column(Enum(TransactionType), nullable=False, default=TransactionType.expense)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
