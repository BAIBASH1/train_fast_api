"""
Authentication Utilities.

This module provides utility functions for user authentication, including the creation of access tokens,
password hashing and verification, and user authentication.

Functions:
    - create_access_token: Generates a JWT access token for a user.
    - get_password_hash: Hashes a plain-text password using bcrypt.
    - verify_password: Verifies if a plain-text password matches the hashed password.
    - authenticate_user: Authenticates a user based on email and password.
"""

from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.users.user_dao import UsersDAO
from config import settings


def create_access_token(data: dict) -> str:
    """
    Generates a JWT access token for a user.

    Args:
        data (dict): A dictionary containing the user information to encode in the token.

    Returns:
        str: The generated JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY_FOR_HASH, settings.ALGORITHM_FOR_HASH
    )
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain-text password matches the hashed password.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password to compare with.

    Returns:
        bool: True if the passwords match, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    """
    Authenticates a user based on email and password.

    Args:
        email (EmailStr): The email of the user.
        password (str): The password of the user.

    Returns:
        user: The authenticated user object if successful, otherwise None.
    """
    user = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(
        password, hashed_password=user.hashed_password
    ):
        return user
