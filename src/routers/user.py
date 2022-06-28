from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from src import models, schemas, utils
from src.database import get_db
from fastapi.security import oauth2
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
    except Exception as error:
        print("exists")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {user.email} already exists")
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
