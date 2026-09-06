import csv
import io
from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.database import get_db
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.models.savings import SavingsGoal, SavingsContribution
from app.models.debt import DebtRecord, DebtPaymentRecord
from app.models.bill import RecurringBill
from app.models.budget import CategoryBudget
from app.models.gift_money import GiftMoneyRecord
from app.core.deps import get_current_user

router = APIRouter(prefix="/backup", tags=["backup"])


@router.get("/export")
def export_backup(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    txs = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    goals = db.query(SavingsGoal).filter(SavingsGoal.user_id == current_user.id).all()
    debts = db.query(DebtRecord).filter(DebtRecord.user_id == current_user.id).all()
    bills = db.query(RecurringBill).filter(RecurringBill.user_id == current_user.id).all()
    cbs = db.query(CategoryBudget).filter(CategoryBudget.user_id == current_user.id).all()
    gift_money = db.query(GiftMoneyRecord).filter(GiftMoneyRecord.user_id == current_user.id).all()

    return {
        "transactions": [
            {
                "amount": float(t.amount), "category": t.category, "note": t.note,
                "date": t.date.isoformat(), "type": t.type.value,
            }
            for t in txs
        ],
        "savings_goals": [
            {
                "name": g.name, "icon": g.icon, "target_amount": float(g.target_amount),
                "contributions": [
                    {"amount": float(c.amount), "date": c.date.isoformat()} for c in g.contributions
                ],
            }
            for g in goals
        ],
        "debts": [
            {
                "person_name": d.person_name, "type": d.type.value, "category": d.category,
                "total_amount": float(d.total_amount),
                "paid_amount": float(d.paid_amount),
                "due_date": d.due_date.isoformat() if d.due_date else None,
                "note": d.note,
            }
            for d in debts
        ],
        "recurring_bills": [
            {
                "name": b.name, "amount": float(b.amount), "category": b.category,
                "due_day": b.due_day, "is_active": b.is_active,
            }
            for b in bills
        ],
        "monthly_budget": float(current_user.monthly_budget),
        "category_budgets": {cb.category: float(cb.limit_amount) for cb in cbs},
        "gift_money": [
            {
                "name": g.name, "address": g.address, "amount": float(g.amount),
                "type": g.type.value, "date": g.date.isoformat(), "note": g.note,
            }
            for g in gift_money
        ],
    }


@router.post("/import")
def import_backup(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Toàn bộ xóa + thêm nằm trong 1 transaction, chỉ commit ở cuối cùng:
    # nếu dữ liệu import bị lỗi/thiếu field, rollback() sẽ hoàn tác luôn phần xóa,
    # tránh mất dữ liệu cũ của user khi import thất bại giữa chừng.
    try:
        # Lưu ý: Query.delete() là bulk delete, KHÔNG tự kích hoạt cascade ORM
        # (cascade="all, delete-orphan" chỉ áp dụng khi xóa qua session.delete()).
        # Nên phải xóa savings_contributions trước, nếu không sẽ để sót bản ghi mồ côi.
        old_goal_ids = [
            g.id for g in db.query(SavingsGoal.id).filter(SavingsGoal.user_id == current_user.id).all()
        ]
        if old_goal_ids:
            db.query(SavingsContribution).filter(SavingsContribution.goal_id.in_(old_goal_ids)).delete(
                synchronize_session=False
            )

        # debt_payments tham chiếu cả transactions.id lẫn debts.id -> phải xóa trước cả hai bảng đó.
        old_debt_ids = [
            d.id for d in db.query(DebtRecord.id).filter(DebtRecord.user_id == current_user.id).all()
        ]
        if old_debt_ids:
            db.query(DebtPaymentRecord).filter(DebtPaymentRecord.debt_id.in_(old_debt_ids)).delete(
                synchronize_session=False
            )

        db.query(Transaction).filter(Transaction.user_id == current_user.id).delete()
        db.query(SavingsGoal).filter(SavingsGoal.user_id == current_user.id).delete()
        db.query(DebtRecord).filter(DebtRecord.user_id == current_user.id).delete()
        db.query(RecurringBill).filter(RecurringBill.user_id == current_user.id).delete()
        db.query(CategoryBudget).filter(CategoryBudget.user_id == current_user.id).delete()
        db.query(GiftMoneyRecord).filter(GiftMoneyRecord.user_id == current_user.id).delete()

        for t in payload.get("transactions", []):
            db.add(Transaction(
                user_id=current_user.id, amount=t["amount"], category=t["category"],
                note=t.get("note", ""), date=date.fromisoformat(t["date"]), type=TransactionType(t["type"]),
            ))
        for g in payload.get("savings_goals", []):
            goal = SavingsGoal(
                user_id=current_user.id, name=g["name"], icon=g.get("icon", "🎯"),
                target_amount=g["target_amount"],
            )
            db.add(goal)
            db.flush()
            for c in g.get("contributions", []):
                db.add(SavingsContribution(
                    goal_id=goal.id, amount=c["amount"], date=datetime.fromisoformat(c["date"])
                ))
        for d in payload.get("debts", []):
            db.add(DebtRecord(
                user_id=current_user.id, person_name=d["person_name"], type=d["type"],
                category=d.get("category", "Khác"),
                total_amount=d["total_amount"], paid_amount=d.get("paid_amount", 0),
                due_date=date.fromisoformat(d["due_date"]) if d.get("due_date") else None,
                note=d.get("note", ""),
            ))
        for b in payload.get("recurring_bills", []):
            db.add(RecurringBill(
                user_id=current_user.id, name=b["name"], amount=b["amount"],
                category=b.get("category", "Hóa đơn"), due_day=b["due_day"],
                is_active=b.get("is_active", True),
            ))
        if "monthly_budget" in payload:
            current_user.monthly_budget = payload["monthly_budget"]
        for category, limit in payload.get("category_budgets", {}).items():
            db.add(CategoryBudget(user_id=current_user.id, category=category, limit_amount=limit))
        for gm in payload.get("gift_money", []):
            db.add(GiftMoneyRecord(
                user_id=current_user.id, name=gm["name"], address=gm.get("address", ""),
                amount=gm["amount"], type=gm["type"], date=date.fromisoformat(gm["date"]),
                note=gm.get("note", ""),
            ))

        db.commit()
    except (KeyError, ValueError, TypeError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"File backup thiếu hoặc sai định dạng dữ liệu: {exc}")

    return {"ok": True}


@router.get("/export-csv")
def export_csv(
    scope: str = "month",
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    if scope == "month" and year and month:
        query = query.filter(
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
    txs = query.order_by(Transaction.date).all()

    output = io.StringIO()
    output.write("\ufeff")  # BOM cho Excel đọc đúng UTF-8
    writer = csv.writer(output)
    writer.writerow(["Ngày", "Loại", "Danh mục", "Ghi chú", "Số tiền"])
    for t in txs:
        writer.writerow([
            t.date.strftime("%d/%m/%Y"),
            "Thu" if t.type == TransactionType.income else "Chi",
            t.category, t.note, int(t.amount),
        ])
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=giao_dich.csv"},
    )
