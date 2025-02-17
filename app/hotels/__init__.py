"""
Hotels Module Package

This package includes all components for managing hotels, including querying hotel information,
room availability, and interacting with bookings. The module contains DAOs, models, schemas, and
routers for handling hotels and related operations like finding hotels by location, availability,
and retrieving detailed information about rooms.

Modules:
    - dao: Contains DAOs for interacting with the database related to hotels and rooms.
    - models: Contains the models representing hotels and rooms in the database.
    - schemas: Contains Pydantic schemas for validating and serializing hotel and room data.
    - router: Contains FastAPI routers for managing API endpoints for hotel operations.
"""

from app.hotels.dao import HotelsDAO
from app.hotels.models import Hotels
from app.hotels.schemas import HotelsRoomsLeftSchema
from app.hotels.router import router

__all__ = ["HotelsDAO", "Hotels", "HotelsRoomsLeftSchema", "router"]
