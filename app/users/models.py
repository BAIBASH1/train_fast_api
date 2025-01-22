from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    bookings: Mapped[list["Bookings"]] = relationship(
        back_populates="user",
    )

