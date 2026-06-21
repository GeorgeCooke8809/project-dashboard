import pytest
import projects
import projects.db as db
from projects.models import Project

class TestAddProject:
    def test_add_one_project_with_description(self):
        projects.utils.add_project("Title", "URL", "Description")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.name == "Title"
        assert project.url == "URL"
        assert project.description == "Description"

    def test_add_one_project_without_description(self):
        projects.utils.add_project("Title", "URL")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.name == "Title"
        assert project.url == "URL"
        assert project.description == None