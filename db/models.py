from datetime import datetime, timedelta
from typing import List

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, SmallInteger, String, Text, func, update
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
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    enabled = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean(), default=False)

    @classmethod
    def clear_user_history(cls, user_id: int):
        session = DB.session()
        session.execute(update(ModelInput).where(ModelInput.user_id == user_id).values(is_deleted=True))
        session.execute(update(Message).where(Message.user_id == user_id).values(is_deleted=True))
        session.execute(update(Topic).where(Topic.user_id == user_id).values(is_deleted=True))
        session.execute(update(Prefix).where(Prefix.user_id == user_id).values(is_deleted=True))
        session.commit()

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
            )
            session.add(user)
            if model_input:
                model = ModelInput(
                    user_id=user_id,
                    model_name=model_input
                )
                session.add(model)
            session.commit()
        return user

    def __str__(self):
        return f"{self.name} ({self.user_id})"


class ModelInput(Base):
    __tablename__ = "talkingwithai_model_input"
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id", ondelete="CASCADE"), index=True)
    user = relationship("User", backref=backref("model_inputs"))
    model_name = Column(String(256), nullable=False)
    is_deleted = Column(Boolean(), default=False)

    @classmethod
    def get_for_user(cls, user_id: int) -> List[str]:
        session = DB.session()
        messages = session.query(cls.model_name).filter(cls.user_id == user_id, cls.is_deleted == False).all()
        return list(zip(*messages))[0] if messages else []


class Message(Base):
    __tablename__ = "talkingwithai_message"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id", ondelete="CASCADE"), index=True)
    user = relationship("User", backref=backref("messages"))
    content = Column(Text, nullable=False)
    is_from_user = Column(Boolean, nullable=False, index=True)
    timestamp = Column(TIMESTAMP, nullable=False, default=func.now())
    is_deleted = Column(Boolean(), default=False)

    @classmethod
    def get_user_messages_for_user(cls, user_id: int) -> List[str]:
        session = DB.session()
        messages = session.query(cls.content) \
            .filter(cls.user_id == user_id, cls.is_from_user == True, cls.is_deleted == False) \
            .all()
        return list(zip(*messages))[0] if messages else []

    @classmethod
    def get_bot_messages_for_user(cls, user_id: int) -> List[str]:
        session = DB.session()
        messages = session.query(cls.content) \
            .filter(cls.user_id == user_id, cls.is_from_user == False, cls.is_deleted == False)
        return [message[0] for message in messages]

    @classmethod
    def add_bot_message(cls, user_id: int, content: str):
        cls.create(user_id, content, is_from_user=False)

    @classmethod
    def add_user_message(cls, user_id: int, content: str):
        cls.create(user_id, content, is_from_user=True)

    @classmethod
    def get_active_users_for_last_days(cls, days: int) -> int:
        session = DB.session()
        return session.query(cls.user_id) \
            .filter(datetime.now() - cls.timestamp <= timedelta(days=days)) \
            .distinct() \
            .count()

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
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id", ondelete="CASCADE"), index=True)
    user = relationship("User", backref=backref("topics"))
    topic = Column(String(256), nullable=False)
    is_deleted = Column(Boolean(), default=False)

    @classmethod
    def add(cls, user_id: int, topic: str):
        session = DB.session()
        topic = cls(user_id=user_id, topic=topic)
        session.add(topic)
        session.commit()


class Prefix(Base):
    __tablename__ = "talkingwithai_prefix"

    prefix_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("talkingwithai_user.user_id", ondelete="CASCADE"), index=True)
    user = relationship("User", backref=backref("prefixes"))
    prefix = Column(String(2048), nullable=False)
    is_deleted = Column(Boolean(), default=False)

    @classmethod
    def get_for_user(cls, user_id: int) -> List[str]:
        session = DB.session()
        prefixes = session.query(cls.prefix).filter(cls.user_id == user_id, cls.is_deleted == False)
        return [prefix[0] for prefix in prefixes]

    @classmethod
    def add(cls, user_id: int, prefix: str):
        session = DB.session()
        prefix = cls(user_id=user_id, prefix=prefix)
        session.add(prefix)
        session.commit()

    @classmethod
    def delete_persona(cls, user_id: int):
        session = DB.session()
        session.execute(
            update(cls).where(cls.user_id == user_id, cls.prefix.ilike('%your persona:%')).values(is_deleted=True)
        )
        session.commit()
