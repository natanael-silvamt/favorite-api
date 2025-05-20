from fastapi import APIRouter

from src.auth.controller import router as auth
from src.client.controller import router as clients
from src.favorite.controller import router as favorites
from src.healthchecks.controller import router as healthchecks

api_router = APIRouter()
api_router.include_router(healthchecks)
api_router.include_router(clients)
api_router.include_router(favorites)
api_router.include_router(auth)
