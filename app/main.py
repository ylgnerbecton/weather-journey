import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pymongo.errors import OperationFailure

from pydantic import ValidationError

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import Settings
from app.presentation.views.healthz import health_check_router
from app.presentation.views.local_weather import LocalWeatherView

settings = Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    application = FastAPI(root_path=settings.API_ROOT_PATH)
    application.state.limiter = Limiter(key_func=get_remote_address)

    add_middleware(application)
    add_routes(application)

    return application


def add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE"],
        allow_headers=["*"],
    )


def add_routes(app: FastAPI):
    app.include_router(health_check_router, prefix="/api/v1")
    app.include_router(LocalWeatherView.router, prefix="/api/v1")


app = create_app()


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url} {process_time}s Exception: {str(e)}"
        )
        raise e from None
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url} {response.status_code} {process_time}s"
    )
    return response


@app.exception_handler(OperationFailure)
async def handle_operation_failure(request: Request, exc: OperationFailure):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


if settings.ENVIRONMENT_NAME == "dev":
    import uvicorn

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8010)
