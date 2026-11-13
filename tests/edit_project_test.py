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

    def test_edit_project_ai_collaboration(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, ai_collaboration=4)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 4

    def test_edit_project_ai_collaboration_to_zero(self):
        projects.utils.add_project("Title", "URL", "edited title description", ai_collaboration=3)
        projects.utils.edit_project(1, ai_collaboration=0)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 0

    def test_edit_project_ai_collaboration_highest(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, ai_collaboration=5)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 5

    def test_edit_project_ai_collaboration_too_high_not_changed(self):
        projects.utils.add_project("Title", "URL", "edited title description", ai_collaboration=2)
        projects.utils.edit_project(1, ai_collaboration=6)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 2

    def test_edit_project_ai_collaboration_too_low_not_changed(self):
        projects.utils.add_project("Title", "URL", "edited title description", ai_collaboration=2)
        projects.utils.edit_project(1, ai_collaboration=-1)

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 2

    def test_edit_project_ai_collaboration_invalid_type_not_changed(self):
        projects.utils.add_project("Title", "URL", "edited title description", ai_collaboration=2)
        projects.utils.edit_project(1, ai_collaboration="4")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.ai_collaboration == 2

    def test_edit_project_github_link(self):
        projects.utils.add_project("Title", "URL", "edited title description")
        projects.utils.edit_project(1, github_link="github.com/GeorgeCooke8809/project-dashboard")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.github_link == "github.com/GeorgeCooke8809/project-dashboard"

    def test_edit_project_github_link_not_changed(self):
        projects.utils.add_project("Title", "URL", "edited title description", github_link="github.com/GeorgeCooke8809/project-dashboard")
        projects.utils.edit_project(1, name="New Title")

        Session = db.Session()
        project = Session.get(Project, 1)
        Session.close()

        assert project.github_link == "github.com/GeorgeCooke8809/project-dashboard"

    def test_no_project_exists(self):
        with pytest.raises(ValueError):
            projects.utils.edit_project(1, name="Name")