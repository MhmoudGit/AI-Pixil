from typing import Any, Sequence

from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from core.models.stickers import Stickers
from core.schemas.stickers import Sticker
from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from core.services.sticker import (
    create_sticker,
    get_all_stickers_from_db,
    get_single_sticker_from_db,
    save_sticker_to_db,
)
from core.settings import templates

router = APIRouter(
    prefix="",
    tags=["Stickers"],
)


@router.get("/sticker-form", response_class=HTMLResponse)
async def sticker_form(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            "templates/generateStk.html", {"request": request}
        )
    else:
        return RedirectResponse(url="/")


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
