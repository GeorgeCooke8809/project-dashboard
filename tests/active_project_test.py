import pytest
import projects
import projects.db as db
from projects.models import Project

class TestActivateProject:
    def test_activate_project(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.deactivate_project(1) # For when the project is active after creation

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.active == False

        projects.utils.activate_project(1)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.active == True

    def test_activate_project_when_already_active(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.activate_project(1)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.active == True
    
    def test_no_project_exists(self):
        with pytest.raises(ValueError):
            projects.utils.activate_project(1)