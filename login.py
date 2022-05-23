import email
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
import db
from functions import find_user_pass
from logout import user_login, user_logout

login_router = APIRouter()
logout_router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    refresh_token: str


class AuthUser(BaseModel):
    username: str
    password: str


class LogoutUser(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = None
    logout: Optional[bool] = None
    password: bool


class UserInDB(UserBase):
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(user_email: str):
    password, is_active, is_logout, resource_id = find_user_pass(user_email)

    return UserInDB(resource_id=resource_id,email=user_email,disable=is_active,password=password,logout=is_logout,)


def authenticate_user(user_email: str, password: str, database: Session):
    password, is_active, logout = find_user_pass(user_email, database=database)

    return UserInDB(email=user_email,disable=is_active,password=password,logout=logout,)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
        return {"email id not found"}
    token_data = TokenData(email=email)
    user = get_user(user_email=token_data.email)

    if user is None:
        return {"USER NOT FOUND"}


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.disabled:
        data = "User With Email ID {} , Disabled User".format(str(current_user.email))
    if current_user.logout:
        return current_user


@login_router.post("", response_model=Token)
async def login_for_access_token(data: AuthUser, database: Session = Depends(db.get_db)):
    user = authenticate_user(data.username, data.password, database=database)
    if not user:
        return {"USER NOT FOUND !!"}
    user_login(database=database, user_email=user.email)
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@logout_router.post("/logout")
async def logout_endpoint(current_user: UserBase = Depends(get_current_active_user)):
    if not current_user:
        return {"wrong credentials"}
    user_logout(current_user.email)

    return {"message": "success"}
