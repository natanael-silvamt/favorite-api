from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database import init_db
from src.routers import api_router

app = FastAPI(
    title="Favorite API",
    description="API for managing clients and their favorite products",
    version="0.0.1",
    openapi_url=f"{settings.API_BASE_URL}/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(api_router, prefix=settings.API_BASE_URL)
