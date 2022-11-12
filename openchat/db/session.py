from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import get_postgres_url


class DB(object):
    _session = None
    _engine = None

    @classmethod
    def session(cls) -> Session:
        return cls._session

    @classmethod
    def engine(cls):
        return cls._engine

    @classmethod
    def remove(cls):
        cls._session = None
        cls._engine = None

    @classmethod
    def init_database_interface(cls):
        if cls._session:
            raise ValueError("Database has already been initialized")
        cls._engine = create_engine(get_postgres_url(), echo=True)
        cls._session = Session(cls._engine)
        # if not cls._engine.has_table("talkingwithai_user"):
        #     raise ValueError('The database is empty. '
        #                      'Please initialize the database with "python ./openchat/db/init_db.py"')

    @classmethod
    def del_database_interface(cls):
        if not cls._session:
            raise ValueError("Database interface hasn't been initialized")
        cls._session = None
        cls._engine = None

    @classmethod
    def is_database_interface_initialized(cls):
        return cls._session is not None
