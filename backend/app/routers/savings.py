from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.savings import SavingsGoal, SavingsContribution
from app.schemas.savings import (
    SavingsGoalCreate,
    SavingsGoalUpdate,
    SavingsGoalRead,
    ContributionCreate,
    ContributionRead,
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/savings", tags=["savings"])


def _get_goal_or_404(db: Session, goal_id: int, user_id: int) -> SavingsGoal:
    goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == user_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục tiêu")
    return goal


@router.get("", response_model=list[SavingsGoalRead])
def list_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(SavingsGoal).filter(SavingsGoal.user_id == current_user.id).all()


@router.post("", response_model=SavingsGoalRead)
def create_goal(payload: SavingsGoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = SavingsGoal(**payload.model_dump(), user_id=current_user.id)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.put("/{goal_id}", response_model=SavingsGoalRead)
def update_goal(goal_id: int, payload: SavingsGoalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = _get_goal_or_404(db, goal_id, current_user.id)
    for key, value in payload.model_dump().items():
        setattr(goal, key, value)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = _get_goal_or_404(db, goal_id, current_user.id)
    db.delete(goal)
    db.commit()
    return {"ok": True}


@router.post("/{goal_id}/contributions", response_model=ContributionRead)
def add_contribution(goal_id: int, payload: ContributionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = _get_goal_or_404(db, goal_id, current_user.id)
    contribution = SavingsContribution(
        goal_id=goal.id, amount=payload.amount, date=payload.date or datetime.utcnow()
    )
    db.add(contribution)
    db.commit()
    db.refresh(contribution)
    return contribution


@router.put("/{goal_id}/contributions/{contribution_id}", response_model=ContributionRead)
def update_contribution(goal_id: int, contribution_id: int, payload: ContributionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _get_goal_or_404(db, goal_id, current_user.id)
    contribution = db.query(SavingsContribution).filter(
        SavingsContribution.id == contribution_id, SavingsContribution.goal_id == goal_id
    ).first()
    if not contribution:
        raise HTTPException(status_code=404, detail="Không tìm thấy lần nạp")
    contribution.amount = payload.amount
    if payload.date:
        contribution.date = payload.date
    db.commit()
    db.refresh(contribution)
    return contribution


@router.delete("/{goal_id}/contributions/{contribution_id}")
def delete_contribution(goal_id: int, contribution_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _get_goal_or_404(db, goal_id, current_user.id)
    contribution = db.query(SavingsContribution).filter(
        SavingsContribution.id == contribution_id, SavingsContribution.goal_id == goal_id
    ).first()
    if not contribution:
        raise HTTPException(status_code=404, detail="Không tìm thấy lần nạp")
    db.delete(contribution)
    db.commit()
    return {"ok": True}
