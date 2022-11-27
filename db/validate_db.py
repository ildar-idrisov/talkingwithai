from db.session import DB


def validate_db():
    DB.init_database_interface()
    DB.validate_database()


if __name__ == '__main__':
    validate_db()
