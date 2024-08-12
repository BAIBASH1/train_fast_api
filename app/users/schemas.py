from pydantic import BaseModel, EmailStr


class UsersAuthSchema(BaseModel):
    email: EmailStr
    password: str
