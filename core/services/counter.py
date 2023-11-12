from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.counter import Counter


async def count_views(db: AsyncSession) -> Column[int]:
    add = Counter()
    db.add(add)
    await db.commit()
    await db.refresh(add)
    return add.id
