from sqlalchemy import Column, Integer
from core.database import Base


class Counter(Base):
    __tablename__: str = "counter"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    views = Column(Integer, nullable=False)
