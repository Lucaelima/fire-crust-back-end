from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import MenuItem
from app.schemas import MenuItemCreate, MenuItemRead

router = APIRouter(prefix="/menu-items", tags=["menu"])


@router.get("", response_model=list[MenuItemRead])
async def list_menu_items(db: AsyncSession = Depends(get_db)) -> list[MenuItemRead]:
    result = await db.execute(select(MenuItem).where(MenuItem.is_available.is_(True)).order_by(MenuItem.name))
    return [MenuItemRead.model_validate(item) for item in result.scalars().all()]


@router.post("", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
async def create_menu_item(payload: MenuItemCreate, db: AsyncSession = Depends(get_db)) -> MenuItemRead:
    duplicate = await db.execute(select(MenuItem).where(MenuItem.name == payload.name))
    if duplicate.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Menu item already exists")

    item = MenuItem(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return MenuItemRead.model_validate(item)
