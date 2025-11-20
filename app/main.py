from fastapi import FastAPI

from app.auth.auth_router import auth_router
from app.bots.bots_router import bots_router
from app.core.utils.lifespan import lifespan

app = FastAPI(
    title="VkBots",
    lifespan=lifespan
)
app.include_router(auth_router)
app.include_router(bots_router)



@app.get("/")
async def main():
    return {"message": "Hello World"}