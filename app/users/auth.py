from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from secrets import token_bytes
from base64 import b64encode
from pydantic import EmailStr

from app.users.dao import UsersDAO
from config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY_FOR_HASH, settings.ALGORITHM_FOR_HASH
    )
    return encoded_jwt


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, hashed_password=user.hashed_password):
        return user

