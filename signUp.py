from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pydantic import EmailStr
from sqlalchemy.orm import Session
import db
import functions

signUp_ops_router = APIRouter()
signUp_client_router = APIRouter()


class UserDetails(BaseModel):
    email: EmailStr
    password: str
    is_ops: bool
    is_active: bool
    is_logout: bool

@signUp_ops_router.post("/Ops_Signup/")
def signup_ops(user_data: UserDetails, database: Session = Depends(db.get_db)):
    user = functions.check_user_exist(database, user_data.email)

    if user:
        raise HTTPException(status_code=409,
                            detail="Email already registered.")
    Ops_user = db.User(email=user_data.email,password=user_data.password,is_ops=True,is_active=True,is_logout=False)

    signedup_user = functions.create_user(database, Ops_user)
    return {"status": "registered successfully","data": signedup_user}


@signUp_client_router.post("/Client_Signup/")
def signup_client(user_data: UserDetails, database: Session = Depends(db.get_db)):
    user = functions.check_user_exist(database, user_data.email)
    if user:
        raise HTTPException(status_code=409,detail="Email already registered.")
    new_user = db.User(email=user_data.email,password=user_data.password,is_ops=False,is_active=True,is_logout=False)
    signedup_user = functions.create_user(database, new_user)
    return {"status": "registered successfully","data": signedup_user}
