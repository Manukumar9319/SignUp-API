import db
from sqlalchemy.orm import Session


def user_login(database: Session, user_email: str):
    data = (database.query(db.User).filter(db.User.email == user_email).first())
    if not data:
        return {"Record Not Found"}
    db.logout = False
    database.commit()


def user_logout(database: Session, user_email: str):
    data = (database.query(db.User).filter(db.User.email == user_email).first())
    if not data:
        return {"Record Not Found"}
    db.is_logout = True
    database.commit()
