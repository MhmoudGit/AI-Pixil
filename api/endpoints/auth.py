from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from core.settings import settings
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError

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
    user = request.session.get("user")
    if user:
        name = user.get("name")
        img = user.get("picture")
        return HTMLResponse(
            f"<p>Hello {name}!</p> <img src={img} /><a href=/logout>Logout</a>"
        )
    return HTMLResponse("<a href=/login>Login</a>")


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for(
        "auth"
    )  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url="/in")
    # return access_token
    user_data = access_token["userinfo"]
    request.session["user"] = dict(user_data)
    return RedirectResponse(url="/in")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/in")
