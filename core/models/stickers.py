from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from core.database import Base


class Stickers(Base):
    __tablename__: str = "stickers"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    sticker = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
