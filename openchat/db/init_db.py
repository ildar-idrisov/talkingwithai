from openchat.db.base import Base
from openchat.db.session import DB


def init_db():
    DB.init_database_interface()
    Base.metadata.create_all(DB.engine())
    DB.validate_database()


if __name__ == '__main__':
    init_db()
