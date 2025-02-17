"""
Hotel rooms Module Package

This package includes all components for managing hotels, rooms, and related bookings.
It contains Data Access Objects (DAO), models, schemas, and API routers necessary for handling
hotel and room data, as well as querying room availability and booking details.

Modules:
    - dao: Contains DAOs for interacting with the database related to rooms and hotels.
    - models: Contains the models representing rooms, hotels, and related entities in the database.
    - schemas: Contains Pydantic schemas for validating and serializing room and hotel data.
    - router: Contains FastAPI routers for managing API endpoints for hotel and room operations.
"""

from app.hotels.rooms.room_dao import RoomsDAO
from app.hotels.rooms.room_models import Rooms
from app.hotels.rooms.room_router import router
from app.hotels.rooms.room_schemas import HotelRoomsSchema

__all__ = ["RoomsDAO", "Rooms", "HotelRoomsSchema", "router"]
