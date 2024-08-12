from pydantic import BaseModel, Json
from datetime import date


class BookingsSchema(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str | None
    services: list[str]
