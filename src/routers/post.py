
from typing import List, Optional

from src import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from src.database import get_db
from sqlalchemy.orm import Session, Query
import src.oauth2 as oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#, response_model=List[schemas.PostResponse]
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit:int=10,skip:int=0,search:Optional[str]=''):
    posts_new:Query = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Post.id==models.Votes.post_id, isouter=True).group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    print(posts_new)
    return posts_new.all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreate)
def create_posts(newPost: schemas.PostCreate, db: Session = Depends(get_db), user_id:int = Depends(oauth2.get_current_user)):
    newPostObject = models.Post(owner_id=user_id,**newPost.dict())

    db.add(newPostObject)
    db.commit()
    db.refresh(newPostObject)

    return newPostObject


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Post.id==models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id:int=Depends(oauth2.get_current_user)):
    delete_post_sql = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post_sql.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")

    if not int(post.owner_id) == int(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to delete this {post.created_by_user_id}post{user_id}")
    delete_post_sql.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT, response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id:int=Depends(oauth2.get_current_user)):
    update_sql = db.query(models.Post).filter(models.Post.id == id)
    post = update_sql.first()

    if not update_sql.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {id} not found")
    if not int(post.owner_id) == int(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to change this {post.owner_id}post{user_id}")
    update_sql.update(updated_post.dict())
    db.commit()
    return update_sql.first()
