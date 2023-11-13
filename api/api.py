import io
from typing import Any, Sequence
from fastapi import APIRouter, Depends, File, Form, Request, Response, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import EmailStr
from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.models.images import Images
from core.models.stickers import Stickers
from core.schemas.images import Image
from core.schemas.stickers import Sticker
from core.services.counter import count_views
from core.services.email import email_create
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


# ----------------------------------------------- view routes
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/home-page", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("templates/home.html", {"request": request})


@router.get("/image-form", response_class=HTMLResponse)
async def image_form(request: Request):
    return templates.TemplateResponse("templates/generateImg.html", {"request": request})


@router.get("/sticker-form", response_class=HTMLResponse)
async def sticker_form(request: Request):
    return templates.TemplateResponse("templates/generateStk.html", {"request": request})


# ------------------------------------------------- api routes
@router.post("/generat-image")
async def generate_image(
    request: Request,
    prompt: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    query = Query(settings.api_url, settings.api_token, prompt)
    res: Response = await query.get_image()
    image = io.BytesIO(res.content)
    await query.save_image(image)
    id: Column[int] = await query.save_to_db(db)
    image: Images = await get_single_image_from_db(id, db)
    return templates.TemplateResponse(
        "templates/singleImage.html", {"request": request, "image": image}
    )


@router.get("/images", response_model=list[Image])
async def images(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Any:
    images_list: Sequence[Images] = await get_all_images_from_db(db)
    return templates.TemplateResponse(
        "templates/images.html", {"request": request, "images": images_list}
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
    request: Request,
    image: UploadFile = File(...),
    sticker_name: str = Form(...),
    for_humans: bool = Form(False),
    db: AsyncSession = Depends(get_session),
) -> Any:
    saved_at: str = await create_sticker(image, sticker_name, for_humans)
    id: Column[int] = await save_sticker_to_db(saved_at, sticker_name, db)
    sticker: Stickers = await get_single_sticker_from_db(id, db)
    return templates.TemplateResponse(
        "templates/singleSticker.html", {"request": request, "sticker": sticker}
    )


@router.get("/stickers", response_model=list[Sticker])
async def stickers(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Any:
    stickers_list: Sequence[Stickers] = await get_all_stickers_from_db(db)
    return templates.TemplateResponse(
        "templates/stickers.html", {"request": request, "stickers": stickers_list}
    )


@router.get("/sticker", response_model=Sticker)
async def sticker(
    id: int,
    db: AsyncSession = Depends(get_session),
) -> Any:
    sticker: Stickers = await get_single_sticker_from_db(id, db)
    return sticker


@router.post("/send_email", response_class=HTMLResponse)
async def post_email(
    email: EmailStr = Form(...),
    db: AsyncSession = Depends(get_session),
):
    try:
        await email_create(email, db)
        html_content = """<p> Email Sent successfully </p>"""
        return HTMLResponse(content=html_content, status_code=200)
    except Exception:
        html_content = """<p> Already subscribed </p>"""
        return HTMLResponse(content=html_content, status_code=200)


@router.post("/counter", response_class=HTMLResponse)
async def count(
    db: AsyncSession = Depends(get_session),
):
    try:
        num = await count_views(db)
        html_content = f"""<p> ---viewers: {num} </p>"""
        return HTMLResponse(content=html_content, status_code=200)
    except Exception:
        html_content = """<p> ---viewers: --  </p>"""
        return HTMLResponse(content=html_content, status_code=200)
