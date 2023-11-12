from pydantic import BaseModel
from datetime import datetime


class Image(BaseModel):
    id: int
    image: str
    prompt: str
    created_at: datetime
