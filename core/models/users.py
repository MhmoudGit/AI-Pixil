from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from core.database import Base


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    paid = Column(Boolean, nullable=False, default=False)
    tries_left = Column(Integer, nullable=False, default=5)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
