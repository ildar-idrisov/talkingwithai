from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('postgresql://talkingwithai:talkingwithai@postgres/talkingwithai', echo=True)
session = Session(engine)

