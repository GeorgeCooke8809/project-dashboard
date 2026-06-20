import pytest
import projects

class TestEditProject:
    def test_edit_project_title(self):
        id = projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(id, name = "New Title")