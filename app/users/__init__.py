"""
User Authentication and Management Module.

This package contains components for user authentication, registration, and profile management.
It provides routes, data access objects (DAO), models, and schemas necessary to manage users in the system.

Modules:
    - auth: Provides functions for creating access tokens, password hashing and verification, and user authentication.
    - dao: Contains the `UsersDAO` class for interacting with the database to retrieve and store user data.
    - dependencies: Provides dependencies for extracting and verifying JWT tokens, and retrieving the current authenticated user.
    - models: Contains the `Users` model for interacting with user data in the database.
    - router: Defines the FastAPI routes for logging in, registering, and managing users.
    - schemas: Defines Pydantic schemas for validating and serializing user data.
"""

from .auth import authenticate_user, create_access_token, get_password_hash
from .user_dao import UsersDAO
from .user_dependencies import get_current_user
from .user_models import Users
from .user_router import router
from .user_schemas import UsersAuthSchema

__all__ = ["authenticate_user", "create_access_token", "get_password_hash", "UsersDAO", "get_current_user", "Users", "router", "UsersAuthSchema"]
