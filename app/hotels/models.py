from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base

class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    rooms: Mapped["Rooms"] = relationship(
        back_populates="hotel",
    )

