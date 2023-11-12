from pydantic import BaseModel
from datetime import datetime


class Sticker(BaseModel):
    id: int
    sticker: str
    prompt: str
    created_at: datetime
