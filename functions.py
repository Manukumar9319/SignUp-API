from sqlalchemy.orm import Session
from passlib.context import CryptContext
import db

def check_user_exist(database: Session, email: str):
    print(database)
    return database.query(db.User).filter(db.User.email == email).first()

def get_user(database: Session, email: str):
    return database.query(db.User).filter(db.User.email == email).first()

def create_user(database: Session, user: db.User):
    database.add(user)
    database.commit()
    return user

def find_user_pass(user_email, database: Session):
    data = database.query(db.User).filter(db.User.email == user_email).first()
    if not data:
        return {"Record Not Found"}
    if data.password:
        password = data.password
        disable_status = data.is_active
        logout = data.is_logout
        return password, disable_status, logout

    database.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)
