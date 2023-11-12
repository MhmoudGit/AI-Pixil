from pydantic import BaseModel
from datetime import datetime


class Sticker(BaseModel):
    id: int
    sticker: str
    created_at: datetime
