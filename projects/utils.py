from projects.models import Project
import logging
from datetime import datetime
from sqlalchemy import select
#from projects.db import session as SESSION
from projects.db import with_session

@with_session
def add_project(Session, name: str, url: str, description: str = None):
    created = datetime.now()

    new_project = Project(name = name, url = url, description = description, datetime_created = created)
    logging.info(f"{new_project = }")
    Session.add(new_project)

@with_session
def edit_project(Session):
    pass

@with_session
def get_projects_overview(Session) -> list[dict]:
    pass

@with_session
def get_project_details(Session) -> dict:
    pass