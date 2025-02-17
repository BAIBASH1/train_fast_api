"""
Schemas for Hotel and Room Data.

This module contains Pydantic schemas used for validating and serializing hotel and room data.
It includes a schema for room details, which contains the necessary fields for representing
room information in API responses.

Schemas:
    - HotelRoomsSchema: Represents detailed information about a room in a hotel, including its availability.
"""

from pydantic import BaseModel


class HotelRoomsSchema(BaseModel):
    """
    Schema for representing a room in a hotel with availability information.

    This schema includes details about the room, such as its name, description, price, quantity,
    and the number of available rooms for a specific date range.
    """

    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int
