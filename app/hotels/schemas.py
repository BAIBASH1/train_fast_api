from pydantic import BaseModel, Json


class SHotelsRoomsLeft(BaseModel):
    id: int
    name: str
    location: str
    services: Json
    rooms_quantity: int
    image_id: int
    rooms_left: int
