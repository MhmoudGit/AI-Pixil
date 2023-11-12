from pydantic import BaseModel


class Counter(BaseModel):
    id: int
