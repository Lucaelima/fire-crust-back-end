from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.deps import get_current_user
from app.models import MenuItem, Order, OrderItem, OrderStatus, User
from app.schemas import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[OrderRead]:
    result = await db.execute(
        select(Order)
        .where(Order.customer_id == current_user.id)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )
    return [OrderRead.model_validate(order) for order in result.scalars().all()]


@router.post("", response_model=OrderRead, status_code=201)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderRead:
    menu_item_ids = [item.menu_item_id for item in payload.items]
    result = await db.execute(select(MenuItem).where(MenuItem.id.in_(menu_item_ids), MenuItem.is_available.is_(True)))
    catalog = {item.id: item for item in result.scalars().all()}
    if len(catalog) != len(set(menu_item_ids)):
        raise HTTPException(status_code=400, detail="One or more menu items were not found")

    order = Order(
        customer_id=current_user.id,
        delivery_address=payload.delivery_address,
        notes=payload.notes,
    )
    db.add(order)
    await db.flush()

    total = 0.0
    for item_payload in payload.items:
        menu_item = catalog[item_payload.menu_item_id]
        subtotal = menu_item.price * item_payload.quantity
        total += subtotal
        db.add(
            OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_payload.quantity,
                unit_price=menu_item.price,
            )
        )

    order.total_price = round(total, 2)
    await db.commit()

    result = await db.execute(select(Order).where(Order.id == order.id).options(selectinload(Order.items)))
    created_order = result.scalar_one()
    return OrderRead.model_validate(created_order)
