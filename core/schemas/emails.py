from pydantic import BaseModel, EmailStr
from datetime import datetime


class Email(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
