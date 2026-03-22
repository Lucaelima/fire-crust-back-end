from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.deps import get_current_user
from app.models import Order, OrderStatus, User
from app.schemas import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardSummary:
    total_orders = await db.scalar(select(func.count(Order.id)).where(Order.customer_id == current_user.id))
    open_orders = await db.scalar(
        select(func.count(Order.id)).where(
            Order.customer_id == current_user.id,
            Order.status.in_([OrderStatus.pending, OrderStatus.preparing, OrderStatus.on_the_way]),
        )
    )
    total_spent = await db.scalar(
        select(func.coalesce(func.sum(Order.total_price), 0.0)).where(
            Order.customer_id == current_user.id,
            Order.status != OrderStatus.cancelled,
        )
    )
    return DashboardSummary(
        total_orders=total_orders or 0,
        open_orders=open_orders or 0,
        total_spent=round(float(total_spent or 0.0), 2),
    )
