from fastapi import FastAPI
import src.models as models
from src.database import engine
from src.routers import post, user, auth,vote
from src.config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

