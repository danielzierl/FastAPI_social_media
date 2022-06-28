from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import oauth2
from sqlalchemy.orm import Session
from src.database import get_db
import src.schemas as schemas
import src.database as database
import src.models as models
import src.utils as utils
import src.oauth2 as oauth
from src.utils import pdw_context

router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post("/",response_model=schemas.Token)
def login_user(user_login: oauth2.OAuth2PasswordRequestForm=Depends(),db:Session = Depends(database.get_db)):

    database_user: models.User = db.query(models.User).filter(models.User.email == user_login.username).first()
    if not database_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user not found")
    if not utils.verifyPswd(user_login.password, database_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="incorrect password")
    token = oauth.create_access_token(data={"user_id": database_user.id})

    return {"token": token, "token_type": "bearer"}
