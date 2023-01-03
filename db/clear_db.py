from db.base import Base
from db.models import *  # noqa: F401,F403
from db.session import DB


def clear_db():
    DB.init_database_interface()
    Base.metadata.drop_all(DB.engine())


if __name__ == '__main__':
    clear_db()
