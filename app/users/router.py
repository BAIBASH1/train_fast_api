"""
Authentication and User Routes.

This module defines the FastAPI routes for user authentication, including login,
registration, and user profile management. It supports JWT token authentication for user login.

Endpoints:
    - login_user: Authenticates a user and returns an access token.
    - register_user: Registers a new user and stores the user data.
    - read_user: Retrieves the current authenticated user's information.
    - logout_user: Logs the user out by deleting their access token.
"""

from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import UsersAuthSchema

router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/login")
async def login_user(response: Response, user_data: UsersAuthSchema):
    """
    Logs in a user and provides a JWT access token.

    Args:
        response (Response): The HTTP response where the token will be set as a cookie.
        user_data (UsersAuthSchema): The user's login credentials.

    Returns:
        str: The generated JWT access token.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/register")
async def register_user(user_data: UsersAuthSchema):
    """
    Registers a new user and stores their data.

    Args:
        user_data (UsersAuthSchema): The user's registration information.

    Returns:
        int: The ID of the newly registered user.
    """
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    user_id = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return user_id


@router.get("/me")
async def read_user(current_user: Users = Depends(get_current_user)):
    """
    Retrieves the current authenticated user's information.

    Args:
        current_user (Users): The current authenticated user.

    Returns:
        Users: The user's data.
    """
    return current_user


@router.post("/logout")
async def logout_user(response: Response):
    """
    Logs the user out by deleting their access token.

    Args:
        response (Response): The HTTP response from which the cookie will be deleted.
    """
    response.delete_cookie("booking_access_token")
