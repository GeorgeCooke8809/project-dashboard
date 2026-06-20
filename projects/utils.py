from projects.models import Project
import logging
from datetime import datetime
from sqlalchemy.orm import query
from projects.db import with_session

@with_session
def add_project(Session, name: str, url: str, description: str = None) -> int:
    created = datetime.now()

    new_project = Project(name = name, url = url, description = description, datetime_created = created, active = True)
    logging.info(f"{new_project = }")
    Session.add(new_project)

    Session.flush()

    return new_project.id

@with_session
def edit_project(Session, project_id: int, name: str = None, url: str = None, description: str = None):
    project: Project = Session.get(Project, project_id)

    if project == None:
        raise ValueError(f"No project with given ID exists. {project_id = }")

    logging.info(f"Project To Edit: {project}")

    if name != None: project.name = name
    if url != None: project.url = url
    if description != None: project.description = description


@with_session
def deactivate_project(Session, project_id: int):
    pass

@with_session
def activate_project(Session, project_id: int):
    pass

@with_session
def get_projects_overview(Session) -> list[dict]:
    pass

@with_session
def get_project_details(Session) -> dict:
    pass