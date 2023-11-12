import io
from typing import Any, Sequence
from fastapi import APIRouter, Depends, File, Form, Response, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.models.images import Images
from core.schemas.images import Image
from core.services.query import Query, get_all_images_from_db, get_single_image_from_db
from core.services.sticker import create_sticker, save_sticker_to_db
from core.settings import settings


router = APIRouter(
    prefix="",
    tags=["AI"],
)


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


@router.get("/images", response_model=list[Image])
async def images(
    db: AsyncSession = Depends(get_session),
) -> Any:
    images_list: Sequence[Images] = await get_all_images_from_db(db)
    return images_list


@router.get("/image", response_model=Image)
async def image(
    id: int,
    db: AsyncSession = Depends(get_session),
) -> Any:
    images_list: Sequence[Images] = await get_single_image_from_db(id, db)
    return images_list


@router.post("/generate_sticker")
async def sticker(
    image: UploadFile = File(...),
    sticker_name: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    saved_at: str = await create_sticker(image, sticker_name)
    await save_sticker_to_db(saved_at, sticker_name, db)
    return {"message": "success"}
