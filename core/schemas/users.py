from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    paid: bool = False
    tries_left: int = 5
