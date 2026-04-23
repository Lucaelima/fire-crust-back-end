import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base, get_db
from app.main import app

TEST_ENGINE = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
TestingSessionLocal = async_sessionmaker(TEST_ENGINE, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


async def seed_schema() -> None:
    async with TEST_ENGINE.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def auth_headers(client: AsyncClient) -> dict[str, str]:
    register_payload = {
        "full_name": "Marina Fire",
        "email": "marina@firecrust.com",
        "phone": "11999999999",
        "password": "secret123",
        "default_address": "Rua das Oliveiras, 100",
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_healthcheck():
    await seed_schema()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_customer_order_flow():
    await seed_schema()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        menu_response = await client.post(
            "/api/v1/menu-items",
            json={
                "name": "Pizza Calabresa",
                "description": "Calabresa com cebola roxa",
                "category": "pizza",
                "price": 52.9,
                "is_available": True,
            },
        )
        assert menu_response.status_code == 201
        menu_item = menu_response.json()

        headers = await auth_headers(client)

        order_response = await client.post(
            "/api/v1/orders",
            headers=headers,
            json={
                "delivery_address": "Rua das Oliveiras, 100",
                "notes": "Sem azeitona",
                "items": [{"menu_item_id": menu_item["id"], "quantity": 2}],
            },
        )
        assert order_response.status_code == 201
        order = order_response.json()
        assert order["customer_id"] == 1
        assert order["total_price"] == 105.8
        assert order["status"] == "pending"

        list_response = await client.get("/api/v1/orders", headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        summary_response = await client.get("/api/v1/dashboard/summary", headers=headers)
        assert summary_response.status_code == 200
        assert summary_response.json() == {"total_orders": 1, "open_orders": 1, "total_spent": 105.8}
