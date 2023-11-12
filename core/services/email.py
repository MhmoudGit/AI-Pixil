from pydantic import EmailStr
from core.models.emails import Emails
from sqlalchemy.ext.asyncio import AsyncSession


async def email_create(email: EmailStr, db: AsyncSession):
    d: dict[str, EmailStr] = {"email": email}
    add = Emails(**d)
    db.add(add)
    await db.commit()
    await db.refresh(add)
    return {"msg": "Email sent successfully"}
