from fastapi import FastAPI
from app.database import init_db
from app.images.routes import router as image_router

app = FastAPI()

app.include_router(image_router, prefix="/image", tags=["images"])


@app.on_event("startup")
async def startup():
    await init_db()
