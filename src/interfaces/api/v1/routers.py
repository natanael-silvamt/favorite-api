from fastapi import APIRouter

from src.interfaces.api.v1.controllers import healthchecks

api_router = APIRouter()
api_router.include_router(healthchecks.router)
