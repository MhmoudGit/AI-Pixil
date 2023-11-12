from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from core.database import Base


class Emails(Base):
    __tablename__: str = "emails"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
