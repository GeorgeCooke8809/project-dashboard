import pytest
import projects
import projects.db as db
from projects.models import Project

class TestEditProject:
    def test_edit_project_title(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, name = "New Title")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.name == "New Title"

    def test_edit_project_url(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, url = "New URL")
        
        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.url == "New URL"

    def test_edit_project_description(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, description = "New Description")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.description == "New Description"

    def test_edit_project_all(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, name = "new name", url = "New URL", description = "new description")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.name == "new name"
        assert project.url == "New URL"
        assert project.description == "new description"

    def test_no_project_exists(self):
        with pytest.raises(ValueError):
            projects.utils.edit_project(1, name="Name")