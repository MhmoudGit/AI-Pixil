from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

# env configs:
load_dotenv()
# template_manager.py


templates = Jinja2Templates(directory="./core/views")


class Settings(BaseSettings):
    api_token: str
    api_url: str
    hub_token: str
    db_username: str
    db_password: str
    db_hostname: str
    db_name: str


settings = Settings()
