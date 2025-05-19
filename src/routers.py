from fastapi import APIRouter

from src.healthchecks.controller import router as healthchecks
from src.client.controller import router as clients

api_router = APIRouter()
api_router.include_router(healthchecks)
api_router.include_router(clients)
