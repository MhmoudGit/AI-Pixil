from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from core.database import Base


class Images(Base):
    __tablename__: str = "images"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    image = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
