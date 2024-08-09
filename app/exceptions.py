from fastapi import HTTPException, status


class BookingExceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль или почта пользователя"


class TokenExpiredException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBookedException(BookingExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = "не осталось свободных номеров"
