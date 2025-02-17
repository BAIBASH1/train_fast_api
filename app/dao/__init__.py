"""
DAO Package for Booking Module

This package contains the `BaseDAO` class, which provides generic CRUD operations that can
be inherited by specific DAO classes for interacting with database models. The `BaseDAO`
class includes methods for querying and manipulating data such as finding records by ID,
inserting new records, updating existing records, and deleting records.

Modules:
    - BaseDAO: The base class for data access operations, providing common methods for database interaction.
"""

from app.dao.base import BaseDAO

__all__ = ["BaseDAO"]
