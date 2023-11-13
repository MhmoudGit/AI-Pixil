from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, Form, Request, Response
from core.services.query import Query, get_all_images_from_db, get_single_image_from_db
from core.models.images import Images
from core.schemas.images import Image
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.settings import settings, templates
import io
from typing import Any, Sequence
from sqlalchemy import Column

router = APIRouter(
    prefix="",
    tags=["Images"],
)


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


@router.get("/image-form", response_class=HTMLResponse)
async def image_form(request: Request):
    return templates.TemplateResponse(
        "templates/generateImg.html", {"request": request}
    )
