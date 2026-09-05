from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.budget import CategoryBudget
from app.schemas.budget import BudgetRead, BudgetUpdate
from app.core.deps import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("", response_model=BudgetRead)
def get_budgets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cbs = db.query(CategoryBudget).filter(CategoryBudget.user_id == current_user.id).all()
    return BudgetRead(
        monthly_budget=float(current_user.monthly_budget),
        category_budgets={cb.category: float(cb.limit_amount) for cb in cbs},
    )


@router.put("", response_model=BudgetRead)
def update_budgets(payload: BudgetUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.monthly_budget is not None:
        current_user.monthly_budget = payload.monthly_budget
    if payload.category_budgets is not None:
        db.query(CategoryBudget).filter(CategoryBudget.user_id == current_user.id).delete()
        for category, limit in payload.category_budgets.items():
            db.add(CategoryBudget(user_id=current_user.id, category=category, limit_amount=limit))
    db.commit()
    cbs = db.query(CategoryBudget).filter(CategoryBudget.user_id == current_user.id).all()
    return BudgetRead(
        monthly_budget=float(current_user.monthly_budget),
        category_budgets={cb.category: float(cb.limit_amount) for cb in cbs},
    )
