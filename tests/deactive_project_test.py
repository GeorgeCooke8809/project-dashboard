import pytest
import projects
import projects.db as db
from projects.models import Project

class TestDeactivateProject:
    def test_deactivate_project(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.deactivate_project(1)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.active == False