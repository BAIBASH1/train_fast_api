"""
Booking Module Package

This package includes all the necessary components for managing bookings in the application.
It consists of DAO, models, schemas, and API routes related to bookings.

Modules:
    - dao: Contains the BookingDAO class with asynchronous methods for managing bookings in the database.
    - models: Contains the `Bookings` model for representing booking records in the database.
    - schemas: Contains the Pydantic schemas for validating and serializing booking-related data.
    - router: Contains FastAPI router for handling booking-related API endpoints, such as creating,
              retrieving, and deleting bookings.

The package facilitates the full lifecycle of booking management from database operations to API interaction.
"""

from .booking_dao import BookingDAO
from .booking_models import Bookings
from .booking_router import router
from .booking_schemas import BookingsInfoSchema, BookingsSchema

__all__ = [
    "BookingDAO",
    "Bookings",
    "BookingsSchema",
    "BookingsInfoSchema",
    "router",
]
