from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from datetime import datetime

from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from config import settings
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request) -> str:
    token: str = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY_FOR_HASH, settings.ALGORITHM_FOR_HASH
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
