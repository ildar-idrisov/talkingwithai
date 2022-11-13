from enum import Enum as EnumConstant

from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import backref, relationship

from openchat.db.base import Base
from openchat.db.session import DB


class Tire(EnumConstant):
    """
    Enumeration of possible tires for a user.
    """

    LEVEL_1 = "LEVEL_1"


class User(Base):
    __tablename__ = "talkingwithai_user"
    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(256), nullable=True)
    name = Column(String(256), nullable=True)
    tire = Column(Enum(Tire), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    messages_limit = Column(Integer, nullable=False, default=0)  # 0 - no limit
    model_input = Column(String(256), nullable=True)


class Message(Base):
    __tablename__ = "talkingwithai_message"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id"), index=True)
    user = relationship("User", backref=backref("messages"))
    content = Column(Text, nullable=False)
    is_from_user = Column(Boolean, nullable=False, index=True)
    timestamp = Column(TIMESTAMP, nullable=False, default=func.now())

    @classmethod
    def add_bot_message(cls, user_id: int, content: str):
        cls.create(user_id, content, is_from_user=False)

    @classmethod
    def add_user_message(cls, user_id: int, content: str):
        cls.create(user_id, content, is_from_user=True)

    @classmethod
    def create(cls, user_id: int, content: str, is_from_user: bool):
        session = DB.session()
        msg = cls(user_id=user_id, content=content, is_from_user=is_from_user)
        session.add(msg)
        session.commit()


class Topic(Base):
    __tablename__ = "talkingwithai_topic"

    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id"), index=True)
    user = relationship("User", backref=backref("topics"))
    topic = Column(String(256), nullable=False)

    @classmethod
    def add(cls, user_id: int, topic: str):
        session = DB.session()
        topic = cls(user_id=user_id, topic=topic)
        session.add(topic)
        session.commit()


class Prefix(Base):
    __tablename__ = "talkingwithai_prefix"

    prefix_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id"), index=True)
    user = relationship("User", backref=backref("prefixes"))
    prefix = Column(String(256), nullable=False)

    @classmethod
    def add(cls, user_id: int, prefix: str):
        session = DB.session()
        prefix = cls(user_id=user_id, prefix=prefix)
        session.add(prefix)
        session.commit()
