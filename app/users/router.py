from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException
from app.users.schemas import SUsersAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи']
)


@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/register")
async def register_user(user_data: SUsersAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    user_id = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return user_id


@router.get("/me")
async def read_user(current_user: Users = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
