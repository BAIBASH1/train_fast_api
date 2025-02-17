"""
Schemas for User Authentication.

This module defines Pydantic schemas used for validating user authentication data.
The `UsersAuthSchema` is used for login and registration processes.

Schemas:
    - UsersAuthSchema: Represents the user's email and password for authentication.
"""

from pydantic import BaseModel, EmailStr


class UsersAuthSchema(BaseModel):
    """
    Schema for user authentication data, including email and password.

    This schema is used to validate the data for user login and registration.
    """

    email: EmailStr
    password: str
