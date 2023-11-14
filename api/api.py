from fastapi import APIRouter
from .endpoints.auth import router as auth
from .endpoints.home import router as home
from .endpoints.images import router as images
from .endpoints.stickers import router as stickers
from .endpoints.counter import router as counter
from .endpoints.email import router as email


routers: list[APIRouter] = [
    auth,
    home,
    images,
    stickers,
    counter,
    email,
]
