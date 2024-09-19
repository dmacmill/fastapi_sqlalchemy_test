from fastapi import APIRouter

from app.api.endpoints import medications

router = APIRouter()

router.include_router(
    router=medications.router, prefix="/medications", tags=["medications"]
)
