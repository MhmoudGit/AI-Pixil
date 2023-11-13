from fastapi.responses import HTMLResponse
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from fastapi import APIRouter, Depends, Form

from core.services.email import email_create

router = APIRouter(
    prefix="",
    tags=["Send Email"],
)


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
