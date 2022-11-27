from db.base import Base
from db.models import *  # noqa: F401,F403
from db.session import DB


def init_db():
    DB.init_database_interface()
    Base.metadata.create_all(DB.engine())
    DB.validate_database()


if __name__ == '__main__':
    init_db()
