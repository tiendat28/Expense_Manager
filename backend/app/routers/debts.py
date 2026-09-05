from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.debt import DebtRecord, DebtPaymentRecord
from app.models.transaction import Transaction, TransactionType
from app.schemas.debt import DebtCreate, DebtUpdate, DebtRead, DebtPayment, DebtPaymentRead
from app.core.deps import get_current_user

router = APIRouter(prefix="/debts", tags=["debts"])


def _get_debt_or_404(db: Session, debt_id: int, user_id: int) -> DebtRecord:
    debt = db.query(DebtRecord).filter(DebtRecord.id == debt_id, DebtRecord.user_id == user_id).first()
    if not debt:
        raise HTTPException(status_code=404, detail="Không tìm thấy khoản nợ")
    return debt


def _get_payment_or_404(db: Session, debt_id: int, payment_id: int) -> DebtPaymentRecord:
    payment = db.query(DebtPaymentRecord).filter(
        DebtPaymentRecord.id == payment_id, DebtPaymentRecord.debt_id == debt_id
    ).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lần thanh toán")
    return payment


def _transaction_note(debt: DebtRecord) -> str:
    return f"{'Trả nợ' if debt.type.value == 'owe' else 'Thu nợ'}: {debt.person_name}"


@router.get("", response_model=list[DebtRead])
def list_debts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(DebtRecord).filter(DebtRecord.user_id == current_user.id).all()


@router.post("", response_model=DebtRead)
def create_debt(payload: DebtCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = DebtRecord(**payload.model_dump(), user_id=current_user.id)
    db.add(debt)
    db.commit()
    db.refresh(debt)
    return debt


@router.put("/{debt_id}", response_model=DebtRead)
def update_debt(debt_id: int, payload: DebtUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = _get_debt_or_404(db, debt_id, current_user.id)
    category_changed = payload.category != debt.category
    for key, value in payload.model_dump().items():
        setattr(debt, key, value)

    # Đồng bộ danh mục sang các giao dịch đã sinh ra từ việc thanh toán khoản nợ này,
    # để Tổng quan/Giao dịch gộp đúng nhóm khi user đổi danh mục sau khi đã trả/thu 1 phần.
    if category_changed:
        transaction_ids = [p.transaction_id for p in debt.payments if p.transaction_id]
        if transaction_ids:
            db.query(Transaction).filter(Transaction.id.in_(transaction_ids)).update(
                {"category": debt.category}, synchronize_session=False
            )

    db.commit()
    db.refresh(debt)
    return debt


@router.delete("/{debt_id}")
def delete_debt(debt_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = _get_debt_or_404(db, debt_id, current_user.id)
    db.delete(debt)
    db.commit()
    return {"ok": True}


@router.post("/{debt_id}/payments", response_model=DebtPaymentRead)
def add_payment(debt_id: int, payload: DebtPayment, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = _get_debt_or_404(db, debt_id, current_user.id)
    debt.paid_amount = float(debt.paid_amount) + payload.amount

    # "Tôi nợ" -> trả nợ là tiền ra (chi tiêu). "Cho vay" -> thu nợ là tiền vào (thu nhập).
    tx = Transaction(
        user_id=current_user.id,
        amount=payload.amount,
        category=debt.category or "Khác",
        note=_transaction_note(debt),
        date=(payload.date or datetime.utcnow()).date(),
        type=TransactionType.expense if debt.type.value == "owe" else TransactionType.income,
    )
    db.add(tx)
    db.flush()

    payment = DebtPaymentRecord(
        debt_id=debt.id, amount=payload.amount, date=payload.date or datetime.utcnow(), transaction_id=tx.id
    )
    db.add(payment)

    db.commit()
    db.refresh(payment)
    return payment


@router.put("/{debt_id}/payments/{payment_id}", response_model=DebtPaymentRead)
def update_payment(debt_id: int, payment_id: int, payload: DebtPayment, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = _get_debt_or_404(db, debt_id, current_user.id)
    payment = _get_payment_or_404(db, debt_id, payment_id)

    debt.paid_amount = float(debt.paid_amount) - float(payment.amount) + payload.amount
    payment.amount = payload.amount
    if payload.date:
        payment.date = payload.date

    if payment.transaction_id:
        tx = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
        if tx:
            tx.amount = payload.amount
            tx.date = payment.date.date()

    db.commit()
    db.refresh(payment)
    return payment


@router.delete("/{debt_id}/payments/{payment_id}")
def delete_payment(debt_id: int, payment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    debt = _get_debt_or_404(db, debt_id, current_user.id)
    payment = _get_payment_or_404(db, debt_id, payment_id)

    debt.paid_amount = max(float(debt.paid_amount) - float(payment.amount), 0)
    transaction_id = payment.transaction_id

    db.delete(payment)
    db.flush()

    if transaction_id:
        db.query(Transaction).filter(Transaction.id == transaction_id).delete()

    db.commit()
    return {"ok": True}
