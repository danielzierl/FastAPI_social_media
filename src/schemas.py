from pydantic.class_validators import validator
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import conint

from src import models


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass
    class Config:
        orm_mode = True





class UserResponse(BaseModel):
    email: EmailStr
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    pass


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None

class PostResponse(BaseModel):
    class Inner(BaseModel):
        title: str
        content: str
        published: bool
        id: int
        owner_id: int
        owner: UserResponse

        class Config:
            orm_mode = True
    Post:Inner
    votes:int

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    @validator('dir')
    def must_be_one_or_zero(cls, value):
        if value not in (0, 1):
            raise ValueError("Must be either 1 or 0")
        return value