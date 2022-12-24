from datetime import datetime, timedelta

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, SmallInteger, String, Text, func
from sqlalchemy.orm import backref, relationship

from db.base import Base
from db.session import DB

__all__ = ['User', 'Message', 'Topic', 'Prefix']


class User(Base):
    __tablename__ = "talkingwithai_user"
    user_id = Column(Integer, primary_key=True)
    nickname = Column(String(256), nullable=True)
    name = Column(String(256), nullable=True)
    tire = Column(SmallInteger, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    messages_limit = Column(Integer, nullable=False, default=0)  # 0 - no limit
    model_input = Column(String(256), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    enabled = Column(Boolean, nullable=False, default=True)

    @classmethod
    def get_users_created_for_last_days(cls, days: int) -> int:
        session = DB.session()
        return session.query(cls).filter(datetime.now() - cls.created_at <= timedelta(days=days)).count()

    @classmethod
    def get_create(cls, user_id, nickname=None, name=None, tire=None, is_admin=False, messages_limit=0, model_input=None):
        session = DB.session()
        user = session.query(cls).get(user_id)
        if not user:
            user = User(
                user_id=user_id,
                nickname=nickname,
                name=name,
                tire=tire,
                is_admin=is_admin,
                messages_limit=messages_limit,
                model_input=model_input
            )
            session.add(user)
            session.commit()
        return user

    def __str__(self):
        return f"{self.name} ({self.user_id})"


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
    def get_active_users_for_last_days(cls, days: int) -> int:
        session = DB.session()
        return session.query(cls.user_id).filter(datetime.now() - cls.timestamp <= timedelta(days=days)).distinct().count()

    @classmethod
    def messages_count_for_last_x_minutes(cls, minutes: int) -> int:
        session = DB.session()
        return session.query(cls).filter(datetime.now() - cls.timestamp <= timedelta(minutes=minutes)).count()

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

    @classmethod
    def get_user_prefixes(cls, user_id: int):
        session = DB.session()
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def delete_persona(cls, user_id: int):
        session = DB.session()
        session.query(cls).filter(cls.user_id == user_id, cls.prefix.ilike('%your persona:%')).delete()
        session.commit()
