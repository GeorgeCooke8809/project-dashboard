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

    def test_details_description_html(self):
        projects.utils.add_project("Project 1", "URL 1", "**Bold**")
        details: dict = projects.utils.get_project_details(1)

        assert "<strong>Bold</strong>" in details["description_html"]

    def test_details_no_description_html(self):
        projects.utils.add_project("Project 1", "URL 1")
        details: dict = projects.utils.get_project_details(1)

        assert details["description_html"] == ""

    def test_details_ai_collaboration(self):
        projects.utils.add_project("Project 1", "URL 1", ai_collaboration=4)
        details: dict = projects.utils.get_project_details(1)

        assert details["ai_collaboration"] == 4

    def test_details_default_ai_collaboration(self):
        projects.utils.add_project("Project 1", "URL 1")
        details: dict = projects.utils.get_project_details(1)

        assert details["ai_collaboration"] == 0

    def test_details_github_link(self):
        projects.utils.add_project("Project 1", "URL 1", github_link="github.com/GeorgeCooke8809/project-dashboard")
        details: dict = projects.utils.get_project_details(1)

        assert details["github_link"] == "github.com/GeorgeCooke8809/project-dashboard"

    def test_details_no_github_link(self):
        projects.utils.add_project("Project 1", "URL 1")
        details: dict = projects.utils.get_project_details(1)

        assert details["github_link"] == None

    def test_no_project_exists(self):
        with pytest.raises(ValueError):
            projects.utils.get_project_details(1)