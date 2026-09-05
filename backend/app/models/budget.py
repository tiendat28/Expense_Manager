from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class CategoryBudget(Base):
    __tablename__ = "category_budgets"
    __table_args__ = (UniqueConstraint("user_id", "category", name="uq_user_category"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String, nullable=False)
    limit_amount = Column(Numeric(14, 0), nullable=False)

    user = relationship("User", back_populates="category_budgets")
