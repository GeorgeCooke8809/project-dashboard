from projects.models import Project
import logging
from datetime import datetime
from projects.db import with_session

@with_session
def check_project_exists(Session, project_id: int) -> bool:
    project: Project = Session.get(Project, project_id)

    if project != None:
        return True
    
    return False

@with_session
def add_project(Session, name: str, url: str, description: str = None) -> int:
    """Adds a new project with all of the given parameters

    Args:
        Session (_type_): The SQL Alchemy session
        name (str): The name of the new project
        url (str): The url to access the project (if web-based)
        description (str, optional): _description_. Defaults to None.

    Returns:
        int: _description_
    """
    created = datetime.now()

    new_project = Project(name = name, url = url, description = description, datetime_created = created, active = True)
    logging.info(f"{new_project = }")
    Session.add(new_project)

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
    project: Project = Session.get(Project, project_id)

    if project == None:
        raise ValueError(f"No project with given ID exists. {project_id = }")

    logging.info(f"Project To Deactivate: {project}")

    project.active = False

@with_session
def activate_project(Session, project_id: int):
    project: Project = Session.get(Project, project_id)

    if project == None:
        raise ValueError(f"No project with given ID exists. {project_id = }")

    logging.info(f"Project To Activate: {project}")

    project.active = True

@with_session
def get_active_projects_overview(Session) -> list[dict]:
    projects: list[Project] = Session.query(Project).filter(Project.active == True).order_by(Project.datetime_created).all() # ? Make this order by change with user choice

    project_dicts = []

    for project in projects:
        project_dicts.append({
            "id": project.id,
            "name": project.name,
            "url": project.url
        })

    return project_dicts

@with_session
def get_project_details(Session, project_id: int) -> dict:
    project: Project = Session.get(Project, project_id)

    if project == None:
        raise ValueError(f"No project with given ID exists. {project_id = }")

    logging.info(f"Project To Display: {project}")

    return {
        "id": project.id,
        "name": project.name,
        "url": project.url,
        "description": project.description,
        "created": project.datetime_created
    }

@with_session
def get_inactive_projects(Session) -> list[dict]:
    projects: list[Project] = Session.get(Project).filter(Project.active == False).order_by(Project.datetime_created).all()

    project_dicts = []

    for project in projects:
        project_dicts.append({
            "id": project.id,
            "name": project.name,
            "url": project.url
        })

    return project_dicts