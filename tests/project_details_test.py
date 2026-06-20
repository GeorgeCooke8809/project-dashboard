import pytest
import projects
import projects.db as db
from projects.models import Project

class TestProjectDetails:
    def test_details_description(self):
        projects.utils.add_project("Project 1", "URL 1", "Description 1")
        details: dict = projects.utils.get_project_details(1)

        assert details["id"] == 1
        assert details["name"] == "Project 1"
        assert details["url"] == "URL 1"
        assert details["description"] == "Description 1"

    def test_details_no_description(self):
        projects.utils.add_project("Project 1", "URL 1")
        details: dict = projects.utils.get_project_details(1)

        assert details["id"] == 1
        assert details["name"] == "Project 1"
        assert details["url"] == "URL 1"
        assert details["description"] == None