from typing import List, Optional
from src import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from src.database import get_db
from sqlalchemy.orm import Session, Query
import src.oauth2 as oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(new_vote: schemas.Vote, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
    vote_query: Query = db.query(models.Votes).filter(models.Votes.post_id == new_vote.post_id,
                                                      models.Votes.user_id == user_id)
    post = db.query(models.Post).filter(models.Post.id == new_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"this post doesnt exist")
    found_vote = vote_query.first()
    if new_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {user_id} has already voted on post")
        new_vote:models.Votes = models.Votes(post_id=new_vote.post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exist")
        vote_query.delete()
        db.commit()
        return {"message": "vote deleted"}
