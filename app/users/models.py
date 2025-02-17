"""
User Model.

This module defines the `Users` model, which represents users in the system. It contains
attributes such as email and hashed password. The `Users` model also establishes a relationship
with the `Bookings` model to associate users with their bookings.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    """
    User Model, which represents users in the system.

    This module defines the structure of the `users` table, which contains information
    about the users in the system.

    Attributes:
        - id: The unique identifier for the user.
        - email: The email of the user.
        - hashed_password: The hashed password for user authentication.
        - bookings: A relationship to the `Bookings` model for tracking user bookings.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    bookings: Mapped[list["Bookings"]] = relationship(
        back_populates="user",
    )
