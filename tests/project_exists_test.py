import pytest
import projects
import projects.db as db
from projects.models import Project

class TestCheckProjectExists:
    def test_project_does_exist(self):
        projects.utils.add_project("Title", "URL", "Desc")

        assert projects.utils.check_project_exists(1) == True

    def test_project_does_not_exist(self):
        assert projects.utils.check_project_exists(1) == False

    def test_project_does_exist_of_many(self):
        for i in range(10):
            projects.utils.add_project("Title", "URL", "Desc")

        assert projects.utils.check_project_exists(9) == True

    def test_project_does_not_exist_of_many(self):
        for i in range(10):
            projects.utils.add_project(f"Title {i}", "URL", "Desc")

        assert projects.utils.check_project_exists(11) == False