"""
Dependency Injection for User Authentication.

This module provides dependencies for token extraction, user authentication, and
retrieving the current user. It verifies JWT tokens and ensures the user is authorized
before accessing certain resources.

Functions:
    - get_token: Extracts the JWT token from the request.
    - get_current_user: Retrieves the current authenticated user from the token.
"""

from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.user_dao import UsersDAO
from app.users.user_models import Users
from config import settings


def get_token(request: Request) -> str:
    """
    Extracts the JWT token from the request.

    Args:
        request (Request): The HTTP request containing the token.

    Returns:
        str: The JWT token if present.

    Raises:
        TokenAbsentException: If the token is not found in the request.
    """
    token: str = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    """
    Retrieves the current authenticated user from the JWT token.

    Args:
        token (str): The JWT token extracted from the request.

    Returns:
        Users: The authenticated user object.

    Raises:
        IncorrectTokenFormatException: If the token format is incorrect.
        TokenExpiredException: If the token is expired.
        UserIsNotPresentException: If no user is found in the token.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY_FOR_HASH, settings.ALGORITHM_FOR_HASH
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
