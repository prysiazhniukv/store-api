from fastapi import FastAPI, HTTPException
from src.models.models import UserPost, UserPostIn
from src.routers.post import router as post_router

app = FastAPI()

app.include_router(post_router, prefix="/posts", tags=["posts"])
