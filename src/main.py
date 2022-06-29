from fastapi import FastAPI
import src.models as models
from src.database import engine
from src.routers import post, user, auth,vote
from fastapi.middleware.cors import CORSMiddleware

origins =["*"]

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=[],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

