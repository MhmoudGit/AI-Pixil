from typing import Tuple
from pydantic import EmailStr
from sqlalchemy import Result, Update, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.users import User
from core.models.users import User as user_model


async def new_user(email: EmailStr, db: AsyncSession) -> User:
    user: User = {"email": email}
    add = user_model(**user)
    db.add(add)
    await db.commit()
    await db.refresh(add)
    return user


async def get_user_by_email(email: EmailStr, db: AsyncSession) -> User:
    q: Result[Tuple[User]] = await db.execute(select(user_model).filter_by(email=email))
    user: User | None = q.scalar()
    return user


async def trial(email: EmailStr, db: AsyncSession) -> int:
    user: User = await get_user_by_email(email, db)
    tries: int = user.tries_left - 1
    if tries <= 0:
        tries = 0
    stmt: Update = (
        update(user_model)
        .where(user_model.email == user.email)
        .values(tries_left=tries)
    )
    await db.execute(stmt)
    await db.commit()
    return tries
