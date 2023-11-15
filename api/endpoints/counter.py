from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from fastapi import APIRouter, Depends
from core.services.counter import count_views, get_views, update_views

router = APIRouter(
    prefix="",
    tags=["Views Counter"],
)


@router.post("/counter", response_class=HTMLResponse)
async def count(
    db: AsyncSession = Depends(get_session),
):
    num = await get_views(db)
    try:
        num = await update_views(db, num + 1)
        html_content = f"""<p> ---viewers: {num} </p>"""
        return HTMLResponse(content=html_content, status_code=200)
    except Exception:
        html_content = f"""<p> ---viewers: {num}  </p>"""
        return HTMLResponse(content=html_content, status_code=200)
