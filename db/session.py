from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import get_postgres_url


class DatabaseInterface:

    def __init__(self) -> None:
        self._engine = create_engine(get_postgres_url(), echo=True)
        self._session = Session(self._engine)


class DB:
    _database_interface = None

    @classmethod
    def session(cls) -> Session:
        return cls._database_interface._session

    @classmethod
    def engine(cls):
        return cls._database_interface._engine

    @classmethod
    def init_database_interface(cls):
        if cls._database_interface:
            raise ValueError("Database has already been initialized")
        cls._database_interface = DatabaseInterface()

    @classmethod
    def del_database_interface(cls):
        if not cls._database_interface:
            raise ValueError("Database interface hasn't been initialized")
        cls._database_interface = None

    @classmethod
    def is_database_interface_initialized(cls):
        return cls._database_interface is not None

    @classmethod
    def validate_database(cls):
        if not cls.is_database_interface_initialized():
            raise ValueError("Database interface hasn't been initialized")

        if not cls._database_interface._engine.has_table("talkingwithai_user"):
            raise ValueError('The database is empty. '
                             'Please initialize the database with "python ./db/init_db.py"')
