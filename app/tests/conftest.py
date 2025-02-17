import asyncio
import json
import logging
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.booking.booking_models import Bookings
from app.database import Base, async_session_maker, engine, init_models
from app.hotels.hotel_models import Hotels
from app.hotels.rooms.room_models import Rooms
from app.main import app as fastapi_app
from app.main import startup
from app.users.user_models import Users
from config import settings

init_models()


@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as connection:
        await connection.run_sync(lambda connection: Base.metadata.drop_all(connection))
        await connection.run_sync(
            lambda connection: Base.metadata.create_all(connection)
        )

    def open_mock_csv(model: str) -> list[dict]:
        with open(
            f"app/tests/mock_data/{model}.json", "r", encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
            return data

    hotels = open_mock_csv("hotels")
    rooms = open_mock_csv("rooms")
    users = open_mock_csv("users")
    bookings = open_mock_csv("bookings")
    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def async_session():
    async with async_session_maker() as async_session:
        yield async_session


@pytest.fixture
async def db_transaction(async_session):
    """Фикстура для изоляции тестов с помощью транзакций."""
    async with async_session.begin():
        yield async_session
        await async_session.rollback()


@pytest.fixture(scope="function")
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "v1/auth/login",
            json={"email": "firstuser@user.ru", "password": "firstuser"},
        )
        assert ac.cookies["booking_access_token"]
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def init_redis():
    await startup()


@pytest.fixture(autouse=True)  # автоматическое применение ко всем тестам
def disable_logging():
    # Сохраняем исходный уровень логирования
    original_level = logging.getLogger().level

    # Устанавливаем уровень CRITICAL
    logging.getLogger().setLevel(logging.CRITICAL)

    yield  # здесь выполняются тесты

    # Восстанавливаем исходный уровень
    logging.getLogger().setLevel(original_level)
