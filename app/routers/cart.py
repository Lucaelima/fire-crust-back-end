from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import MenuItem
from app.schemas import CartItem, CartItemsRequest

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/items", response_model=list[CartItem])
async def get_cart_items(
    payload: CartItemsRequest,
    db: AsyncSession = Depends(get_db),
) -> list[CartItem]:
    menu_item_ids = [item.menu_item_id for item in payload.items]
    result = await db.execute(select(MenuItem).where(MenuItem.id.in_(menu_item_ids), MenuItem.is_available.is_(True)))
    catalog = {item.id: item for item in result.scalars().all()}

    if len(catalog) != len(set(menu_item_ids)):
        raise HTTPException(status_code=400, detail="One or more menu items were not found")

    return [
        CartItem(menu_item=catalog[item.menu_item_id], quantity=item.quantity)
        for item in payload.items
    ]
