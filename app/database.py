"""
Database Configuration and Initialization.

This module configures and initializes the database for the application using SQLAlchemy.
It provides the engine and session maker for interacting with the database asynchronously.
It also includes a function for initializing the models in the application.

Attributes:
    async_session_maker (sessionmaker): The session maker for creating database sessions.
    engine (Engine): The SQLAlchemy engine used for interacting with the database.
"""

from datetime import datetime

from sqlalchemy import NullPool, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def init_models():
    """
    Initializes the models for the application by importing them. This ensures that
    all models are registered with SQLAlchemy, alembic and available for database operations.
    """
    from app.booking.booking_models import Bookings  # noqa
    from app.hotels.hotel_models import Hotels  # noqa
    from app.hotels.rooms.room_models import Rooms  # noqa
    from app.users.user_models import Users  # noqa


class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
