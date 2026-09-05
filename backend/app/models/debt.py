import enum
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class DebtType(str, enum.Enum):
    owe = "owe"
    lent = "lent"


class DebtRecord(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    person_name = Column(String, nullable=False)
    type = Column(Enum(DebtType), nullable=False)
    category = Column(String, default="Khác")
    total_amount = Column(Numeric(14, 0), nullable=False)
    paid_amount = Column(Numeric(14, 0), default=0)
    due_date = Column(Date, nullable=True)
    note = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="debts")
    payments = relationship(
        "DebtPaymentRecord", back_populates="debt", cascade="all, delete-orphan", order_by="DebtPaymentRecord.date.desc()"
    )


class DebtPaymentRecord(Base):
    __tablename__ = "debt_payments"

    id = Column(Integer, primary_key=True, index=True)
    debt_id = Column(Integer, ForeignKey("debts.id"), nullable=False, index=True)
    amount = Column(Numeric(14, 0), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)

    debt = relationship("DebtRecord", back_populates="payments")
