"""
Schemas for Hotel Data.

This module defines Pydantic schemas used for validating and serializing hotel data. The `HotelsRoomsLeftSchema`
represents detailed information about hotels, including room availability.

Schemas:
    - HotelsRoomsLeftSchema: Represents detailed information about a hotel, including its available rooms.
"""

from pydantic import BaseModel, Json


class HotelsRoomsLeftSchema(BaseModel):
    """
    Schema for representing a hotel with room availability.

    This schema includes information about the hotel, such as its name, location, services,
    the total number of rooms, the number of rooms left, and an image ID.

    Attributes:
        id (int): The unique identifier for the hotel.
        name (str): The name of the hotel.
        location (str): The location of the hotel.
        services (Json): A JSON representation of the services provided by the hotel.
        rooms_quantity (int): The total number of rooms available in the hotel.
        image_id (int): The ID associated with the hotel's image.
        rooms_left (int): The number of available rooms in the hotel for the specified period.
    """
    id: int
    name: str
    location: str
    services: Json
    rooms_quantity: int
    image_id: int
    rooms_left: int
