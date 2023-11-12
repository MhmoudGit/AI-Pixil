from pydantic import BaseModel
from datetime import datetime


class Sticker(BaseModel):
    id: int
    sticker: str
    name: str
    created_at: datetime
