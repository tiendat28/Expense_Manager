from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, computed_field


class ContributionCreate(BaseModel):
    amount: float
    date: Optional[datetime] = None


class ContributionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: float
    date: datetime


class SavingsGoalCreate(BaseModel):
    name: str
    icon: str = "🎯"
    target_amount: float


class SavingsGoalUpdate(SavingsGoalCreate):
    pass


class SavingsGoalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    icon: str
    target_amount: float
    created_at: datetime
    contributions: List[ContributionRead] = []

    @computed_field
    @property
    def saved_amount(self) -> float:
        return sum(c.amount for c in self.contributions)
