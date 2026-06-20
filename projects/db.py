from configs import DATABASE_URL, DEBUGGING_STATE
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(DATABASE_URL, echo=DEBUGGING_STATE)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def with_session(func):
    def wrap(*args, **kwargs):
        session = Session()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except:
            session.rollback()
        finally:
            session.close()
    return wrap