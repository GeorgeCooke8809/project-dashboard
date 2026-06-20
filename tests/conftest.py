import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import projects.db as db
from projects.db import Base
from projects.models import Project

@pytest.fixture(autouse=True)
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db.Session = TestSession

    yield

    Base.metadata.drop_all(engine)
    