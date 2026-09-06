import enum
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class GiftMoneyType(str, enum.Enum):
    wedding = "wedding"
    sick = "sick"
    newborn = "newborn"


class GiftMoneyRecord(Base):
    __tablename__ = "gift_money"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    address = Column(String, default="")
    amount = Column(Numeric(14, 0), nullable=False)
    type = Column(Enum(GiftMoneyType), nullable=False)
    date = Column(Date, nullable=False)
    note = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="gift_money_records")
