from fastapi import FastAPI
import uvicorn
from api.api import router
from core.database import app_configs


app = FastAPI(**app_configs)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
