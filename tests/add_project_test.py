import pytest
import projects

class TestAddProject: # TODO: Add asserts when you can 
    def test_add_one_project_with_description(self):
        projects.utils.add_project("Title", "URL", "Description")

    def test_add_one_project_without_description(self):
        projects.utils.add_project("Title", "URL")