from sqlalchemy import Column, String, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
SQLALCHEMY_DATABASE_URL = ""
DB_CONNECTION_LINK ="postgresql://{}:{}@{}/{}".format(
    "ez_user", "somepwd123", "127.0.0.1:5432", "ez_delivery"
)

engine = create_engine(DB_CONNECTION_LINK)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()



class User(Base):
    __tablename__ = "USERS"

    email = Column(String, primary_key=True)
    password = Column(String, nullable=True)
    is_ops = Column(Boolean, nullable=True)
    is_active = Column(Boolean, nullable=True)
    is_logout = Column(Boolean, nullable=True)


def get_db():
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()


db = get_db()
Base.metadata.create_all(bind=engine)
