from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from backend.app.api import main_router
from backend.app.core.utils.lifespan import lifespan


def create_app():

    app = FastAPI(
        title="VkBots",
        lifespan=lifespan
    )

    @app.exception_handler(Exception)
    async def common_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Something gone wrong"}
        )

    app.include_router(main_router)

    return app
