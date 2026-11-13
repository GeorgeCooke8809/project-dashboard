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

    def test_add_project_default_ai_collaboration(self):
        projects.utils.add_project("Title", "URL")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 0

    def test_add_project_ai_collaboration(self):
        projects.utils.add_project("Title", "URL", ai_collaboration=3)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 3

    def test_add_project_ai_collaboration_highest(self):
        projects.utils.add_project("Title", "URL", ai_collaboration=5)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 5

    def test_add_project_ai_collaboration_too_high(self):
        with pytest.raises(ValueError):
            projects.utils.add_project("Title", "URL", ai_collaboration=6)

    def test_add_project_ai_collaboration_too_low(self):
        with pytest.raises(ValueError):
            projects.utils.add_project("Title", "URL", ai_collaboration=-1)

    def test_add_project_ai_collaboration_invalid_type(self):
        with pytest.raises(ValueError):
            projects.utils.add_project("Title", "URL", ai_collaboration="3")

    def test_add_project_ai_collaboration_invalid_bool(self):
        with pytest.raises(ValueError):
            projects.utils.add_project("Title", "URL", ai_collaboration=True)

    def test_add_project_invalid_ai_collaboration_not_added(self):
        with pytest.raises(ValueError):
            projects.utils.add_project("Title", "URL", ai_collaboration=6)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project == None

    def test_add_project_github_link(self):
        projects.utils.add_project("Title", "URL", github_link="github.com/GeorgeCooke8809/project-dashboard")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.github_link == "github.com/GeorgeCooke8809/project-dashboard"

    def test_add_project_no_github_link(self):
        projects.utils.add_project("Title", "URL")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.github_link == None