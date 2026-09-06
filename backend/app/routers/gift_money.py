from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.gift_money import GiftMoneyRecord
from app.schemas.gift_money import GiftMoneyCreate, GiftMoneyUpdate, GiftMoneyRead
from app.core.deps import get_current_user

router = APIRouter(prefix="/gift-money", tags=["gift-money"])


def _get_record_or_404(db: Session, record_id: int, user_id: int) -> GiftMoneyRecord:
    record = db.query(GiftMoneyRecord).filter(GiftMoneyRecord.id == record_id, GiftMoneyRecord.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy khoản tiền mừng")
    return record


@router.get("", response_model=list[GiftMoneyRead])
def list_gift_money(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(GiftMoneyRecord)
        .filter(GiftMoneyRecord.user_id == current_user.id)
        .order_by(GiftMoneyRecord.date.desc(), GiftMoneyRecord.id.desc())
        .all()
    )


@router.post("", response_model=GiftMoneyRead)
def create_gift_money(payload: GiftMoneyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = GiftMoneyRecord(**payload.model_dump(), user_id=current_user.id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{record_id}", response_model=GiftMoneyRead)
def update_gift_money(
    record_id: int, payload: GiftMoneyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    record = _get_record_or_404(db, record_id, current_user.id)
    for key, value in payload.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}")
def delete_gift_money(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = _get_record_or_404(db, record_id, current_user.id)
    db.delete(record)
    db.commit()
    return {"ok": True}
