"""This file contains hooks for pytest."""
from unittest.mock import MagicMock

import pytest
from sqlalchemy import MetaData
from sqlalchemy.exc import InternalError
from sqlalchemy_utils import database_exists, create_database

from db.base import Base
from db.session import DB


@pytest.fixture
def session():
    mock_session = _init_test_session()
    yield mock_session
    _remove_test_session(mock_session)


def _init_test_session():
    session = DB.session()
    # this is sanity check - if intermittent failures are gone i will remove it
    for table in reversed(Base.metadata.sorted_tables):
        count = session.query(table).count()
        if not isinstance(count, MagicMock) and count != 0:
            raise ValueError(f"Table {table} already exists data {count}")
    return session


def _remove_test_session(session) -> None:
    # Don't use in tests
    session.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope="session", autouse=True)
def init_database():
    if DB.is_database_interface_initialized():
        DB.del_database_interface()
    DB.init_database_interface()

    if not database_exists(DB.engine().url):
        create_database(DB.engine().url)

    try:
        Base.metadata.drop_all(DB.engine())
    except InternalError:
        # Allows us to delete all db objects including those which
        # aren't presented in actual SauronBase.metadata
        current_metadata = MetaData()
        current_metadata.reflect(bind=DB.engine())
        current_metadata.drop_all(DB.engine())
    Base.metadata.create_all(DB.engine())

    yield
