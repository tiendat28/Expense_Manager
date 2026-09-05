from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.database import get_db
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionRead
from app.core.deps import get_current_user
from fastapi import HTTPException

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
def list_transactions(
    year: int,
    month: int,
    type: Optional[TransactionType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        extract("year", Transaction.date) == year,
        extract("month", Transaction.date) == month,
    )
    if type:
        query = query.filter(Transaction.type == type)
    return query.order_by(Transaction.date.desc()).all()


@router.post("", response_model=TransactionRead)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = Transaction(**payload.model_dump(), user_id=current_user.id)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.put("/{tx_id}", response_model=TransactionRead)
def update_transaction(
    tx_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")
    for key, value in payload.model_dump().items():
        setattr(tx, key, value)
    db.commit()
    db.refresh(tx)
    return tx


@router.delete("/{tx_id}")
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id, Transaction.user_id == current_user.id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Không tìm thấy giao dịch")
    db.delete(tx)
    db.commit()
    return {"ok": True}


@router.get("/stats/monthly")
def monthly_stats(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    txs = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        extract("year", Transaction.date) == year,
        extract("month", Transaction.date) == month,
    ).all()
    income_total = sum(float(t.amount) for t in txs if t.type == TransactionType.income)
    expense_total = sum(float(t.amount) for t in txs if t.type == TransactionType.expense)
    category_totals: dict[str, float] = {}
    for t in txs:
        if t.type == TransactionType.expense:
            category_totals[t.category] = category_totals.get(t.category, 0) + float(t.amount)
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "category_totals": [{"category": c, "total": t} for c, t in sorted_categories],
    }


@router.get("/stats/trend")
def trend_stats(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    result = []
    for i in range(months - 1, -1, -1):
        y, m = today.year, today.month - i
        while m <= 0:
            m += 12
            y -= 1
        txs = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == TransactionType.expense,
            extract("year", Transaction.date) == y,
            extract("month", Transaction.date) == m,
        ).all()
        total_amount = sum(float(t.amount) for t in txs)
        result.append({"year": y, "month": m, "total": total_amount})
    return result
