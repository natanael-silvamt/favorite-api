from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interfaces.api.v1.routers import api_router

app = FastAPI(
    title="Favorite API",
    description="API for managing clients and their favorite products",
    version="0.0.1",
    openapi_url="/api/v1/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1/favorites")
