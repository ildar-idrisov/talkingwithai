from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "talkingwithai_user"
    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(256), nullable=False)