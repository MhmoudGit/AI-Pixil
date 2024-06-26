from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Depends, Form, Request, Response
from core.services.query import Query, get_all_images_from_db, get_single_image_from_db
from core.models.images import Images
from core.schemas.images import Image
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.services.user import trial
from core.settings import settings, templates
import io
from typing import Any, Sequence
from sqlalchemy import Column


router = APIRouter(
    prefix="",
    tags=["Images"],
)


@router.get("/image-form", response_class=HTMLResponse)
async def image_form(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            "templates/generateImg.html", {"request": request}
        )
    else:
        return RedirectResponse(url="/")


@router.post("/generat-image")
async def generate_image(
    request: Request,
    prompt: str = Form(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    user = request.session.get("user")
    if user is not None:
        email: str = user.get("email")
        tries: int = await trial(email, db)
    if tries <= 0:
        html_content: str = f"""<p> {tries} Tries Left -- Subscribe for more  </p>"""
        return HTMLResponse(content=html_content, status_code=200)
    try:
        query = Query(settings.api_url, settings.api_token, prompt)
        res: Response = await query.get_image()
        image = io.BytesIO(res.content)
        await query.save_image(image)
        id: Column[int] = await query.save_to_db(db)
        image: Images = await get_single_image_from_db(id, db)
        return templates.TemplateResponse(
            "templates/singleImage.html",
            {"request": request, "image": image, "tries": tries},
        )
    except Exception:
        html_content: str = """<p> Something went wrong... try again!  </p>"""
        return HTMLResponse(content=html_content, status_code=200)


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
