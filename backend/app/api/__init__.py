from fastapi import APIRouter, status
from fastapi.responses import Response

from backend.app.api.auth.auth_router import auth_router
from backend.app.api.bots.bots_router import bots_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(bots_router)

@main_router.get("/")
async def main_entry_point():
    return Response(
        content="VkBot app api",
        status_code=status.HTTP_200_OK
    )