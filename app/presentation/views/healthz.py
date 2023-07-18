from fastapi import APIRouter

health_check_router = APIRouter(tags=["health"])


@health_check_router.get("/healthz")
async def healthz():
    return {"status": "OK"}


@health_check_router.get("/readiness")
async def readiness():
    return {"status": "OK"}
