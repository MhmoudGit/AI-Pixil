import io
from typing import Any
from fastapi import APIRouter, Depends, Form, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.services.query import Query
from core.settings import settings


router = APIRouter(
    prefix="",
    tags=["AI"],
)


# normal api route for local usage
@router.post("/generat-image")
async def generate_image(
    prompt: str = Form(...), db: AsyncSession = Depends(get_session)
) -> Any:
    query = Query(settings.api_url, settings.api_token, prompt)
    res: Response = await query.get_image()
    image = io.BytesIO(res.content)
    await query.save_image(image)
    await query.save_to_db(db)
    return StreamingResponse(image, media_type=res.headers["content-type"])
