from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from api.api import routers
from core.database import app_configs


app = FastAPI(**app_configs)
app.mount("/static", StaticFiles(directory="./static"), name="static")

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
