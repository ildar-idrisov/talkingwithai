from db.db_connect import engine
from db.models import Base

Base.metadata.create_all(engine)
