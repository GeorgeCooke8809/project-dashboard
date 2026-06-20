from run import DATABASE_URL, DEBUGGING_STATE
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(DATABASE_URL, echo=DEBUGGING_STATE)

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass