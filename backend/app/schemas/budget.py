from typing import Dict, Optional
from pydantic import BaseModel


class BudgetRead(BaseModel):
    monthly_budget: float
    category_budgets: Dict[str, float]


class BudgetUpdate(BaseModel):
    monthly_budget: Optional[float] = None
    category_budgets: Optional[Dict[str, float]] = None
