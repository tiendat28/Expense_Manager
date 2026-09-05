from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class RecurringBill(Base):
    __tablename__ = "recurring_bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    amount = Column(Numeric(14, 0), nullable=False)
    category = Column(String, default="Hóa đơn")
    due_day = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    last_paid_month = Column(String, nullable=True)  # "YYYY-MM"

    user = relationship("User", back_populates="bills")
