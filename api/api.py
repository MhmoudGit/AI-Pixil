import io
from typing import Any, Sequence
from fastapi import APIRouter, Depends, Form, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.models.images import Images
from core.schemas.images import Image
from core.services.query import Query, get_all_images_from_db
from core.settings import settings


router = APIRouter(
    prefix="",
    tags=["AI"],
)


# normal api route for local usage
@router.post("/generat-image")
async def generate_image(
    prompt: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    query = Query(settings.api_url, settings.api_token, prompt)
    res: Response = await query.get_image()
    image = io.BytesIO(res.content)
    await query.save_image(image)
    await query.save_to_db(db)
    return StreamingResponse(image, media_type=res.headers["content-type"])


# normal api route for local usage
@router.get("/images", response_model=list[Image])
async def images(
    db: AsyncSession = Depends(get_session),
) -> Any:
    images_list: Sequence[Images] = await get_all_images_from_db(db)
    return images_list
