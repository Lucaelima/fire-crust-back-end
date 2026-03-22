from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import MenuCategory, OrderStatus


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=30)
    password: str = Field(min_length=6, max_length=64)
    default_address: str = Field(min_length=5, max_length=255)


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    default_address: str

    model_config = ConfigDict(from_attributes=True)


class RegisterResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=400)
    category: MenuCategory
    price: float = Field(gt=0)
    is_available: bool = True


class MenuItemRead(MenuItemCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0, le=20)


class OrderCreate(BaseModel):
    delivery_address: str = Field(min_length=5, max_length=255)
    notes: str = Field(default="", max_length=500)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    customer_id: int
    delivery_address: str
    notes: str
    status: OrderStatus
    total_price: float
    created_at: datetime
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_orders: int
    open_orders: int
    total_spent: float
