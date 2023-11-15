from sqlalchemy import Column, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.counter import Counter


async def count_views(db: AsyncSession) -> Column[int]:
    add = Counter(views=1)
    db.add(add)
    await db.commit()
    await db.refresh(add)
    return add.views


async def get_views(db: AsyncSession):
    q = await db.execute(select(Counter).filter_by(id=1))
    views = q.scalar()
    return views.views


async def update_views(db: AsyncSession, num: int):
    stmt = update(Counter).where(Counter.id == 1).values(views=num)
    await db.execute(stmt)
    await db.commit()
    return num
