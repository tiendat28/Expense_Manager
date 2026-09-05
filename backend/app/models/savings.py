from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class SavingsGoal(Base):
    __tablename__ = "savings_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, default="🎯")
    target_amount = Column(Numeric(14, 0), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="savings_goals")
    contributions = relationship(
        "SavingsContribution", back_populates="goal", cascade="all, delete-orphan"
    )


class SavingsContribution(Base):
    __tablename__ = "savings_contributions"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("savings_goals.id"), nullable=False, index=True)
    amount = Column(Numeric(14, 0), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    goal = relationship("SavingsGoal", back_populates="contributions")
