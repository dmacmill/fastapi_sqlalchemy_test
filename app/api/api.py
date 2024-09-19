from fastapi import APIRouter

from app.api.endpoints import medications, patients, perscriptions

router = APIRouter()

router.include_router(
    router=medications.router, prefix="/medications", tags=["medications"]
)
router.include_router(
    router=patients.router, prefix="/patients", tags=["patients"]
)
router.include_router(
    router=perscriptions.router, prefix="/perscriptions", tags=["perscriptions"]
)