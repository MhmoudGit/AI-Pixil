import io
from typing import Any, Sequence
from fastapi import APIRouter, Depends, File, Form, Request, Response, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.models.images import Images
from core.models.stickers import Stickers
from core.schemas.images import Image
from core.schemas.stickers import Sticker
from core.services.query import Query, get_all_images_from_db, get_single_image_from_db
from core.services.sticker import (
    create_sticker,
    get_all_stickers_from_db,
    get_single_sticker_from_db,
    save_sticker_to_db,
)
from core.settings import settings
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./core/views")

router = APIRouter(
    prefix="",
    tags=["AI"],
)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/home-page", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


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
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Any:
    images_list: Sequence[Images] = await get_all_images_from_db(db)
    return templates.TemplateResponse(
        "images.html", {"request": request, "images": images_list}
    )


@router.get("/image", response_model=Image)
async def image(
    id: int,
    db: AsyncSession = Depends(get_session),
) -> Any:
    image: Images = await get_single_image_from_db(id, db)
    return image


@router.post("/generate_sticker")
async def generate_sticker(
    image: UploadFile = File(...),
    sticker_name: str = Form(...),
    for_humans: bool = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    saved_at: str = await create_sticker(image, sticker_name, for_humans)
    await save_sticker_to_db(saved_at, sticker_name, db)
    return {"message": "success"}


@router.get("/stickers", response_model=list[Sticker])
async def stickers(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Any:
    stickers_list: Sequence[Stickers] = await get_all_stickers_from_db(db)
    return templates.TemplateResponse(
        "stickers.html", {"request": request, "stickers": stickers_list}
    )


@router.get("/sticker", response_model=Sticker)
async def sticker(
    id: int,
    db: AsyncSession = Depends(get_session),
) -> Any:
    sticker: Stickers = await get_single_sticker_from_db(id, db)
    return sticker
