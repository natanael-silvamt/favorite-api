from fastapi import APIRouter

from src.client.controller import router as clients
from src.healthchecks.controller import router as healthchecks

api_router = APIRouter()
api_router.include_router(healthchecks)
api_router.include_router(clients)
