from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from core.settings import templates


router = APIRouter(
    prefix="",
    tags=["Home"],
)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/home-page", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("templates/home.html", {"request": request})
