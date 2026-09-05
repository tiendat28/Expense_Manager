from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.bill import RecurringBill
from app.models.transaction import Transaction, TransactionType
from app.schemas.bill import BillCreate, BillUpdate, BillRead
from app.core.deps import get_current_user

router = APIRouter(prefix="/bills", tags=["bills"])


def _get_bill_or_404(db: Session, bill_id: int, user_id: int) -> RecurringBill:
    bill = db.query(RecurringBill).filter(RecurringBill.id == bill_id, RecurringBill.user_id == user_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn")
    return bill


@router.get("", response_model=list[BillRead])
def list_bills(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(RecurringBill).filter(RecurringBill.user_id == current_user.id).all()


@router.post("", response_model=BillRead)
def create_bill(payload: BillCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bill = RecurringBill(**payload.model_dump(), user_id=current_user.id)
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


@router.put("/{bill_id}", response_model=BillRead)
def update_bill(bill_id: int, payload: BillUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bill = _get_bill_or_404(db, bill_id, current_user.id)
    for key, value in payload.model_dump().items():
        setattr(bill, key, value)
    db.commit()
    db.refresh(bill)
    return bill


@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bill = _get_bill_or_404(db, bill_id, current_user.id)
    db.delete(bill)
    db.commit()
    return {"ok": True}


@router.post("/{bill_id}/toggle-active", response_model=BillRead)
def toggle_active(bill_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bill = _get_bill_or_404(db, bill_id, current_user.id)
    bill.is_active = not bill.is_active
    db.commit()
    db.refresh(bill)
    return bill


@router.post("/{bill_id}/mark-paid", response_model=BillRead)
def mark_paid(
    bill_id: int,
    add_as_expense: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bill = _get_bill_or_404(db, bill_id, current_user.id)
    today = date.today()
    bill.last_paid_month = f"{today.year}-{today.month:02d}"
    if add_as_expense:
        tx = Transaction(
            user_id=current_user.id,
            amount=bill.amount,
            category=bill.category,
            note=bill.name,
            date=today,
            type=TransactionType.expense,
        )
        db.add(tx)
    db.commit()
    db.refresh(bill)
    return bill
