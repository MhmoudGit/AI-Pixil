from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from core.database import get_session
from core.services.user import get_user_by_email, new_user
from core.settings import settings, templates
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="",
    tags=["Google-Auth"],
)

# Set up oauth starlette
config_data: dict[str, str] = {
    "GOOGLE_CLIENT_ID": settings.google_client_id,
    "GOOGLE_CLIENT_SECRET": settings.google_client_secret,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/in")
def public(request: Request):
    return RedirectResponse(url="/")


@router.get("/check_user")
def check_user(request: Request):
    user = request.session.get("user")
    if user is not None:
        name = user.get("name")
        image = user.get("picture")
        return templates.TemplateResponse(
            "templates/auth.html", {"request": request, "name": name, "image": image}
        )
    return templates.TemplateResponse(
        "templates/auth.html", {"request": request, "name": None}
    )


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for(
        "auth"
    )  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url="/in")
    # return access_token
    user_data = access_token["userinfo"]
    request.session["user"] = dict(user_data)
    user = await get_user_by_email(user_data.email, db)
    if not user:
        await new_user(user_data.email, db)
    return RedirectResponse(url="/in")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
