import pytest
import projects
import projects.db as db
from projects.models import Project
import time

class TestActiveProjectsOverview:
    def test_active_projects_overview_single(self):
        projects.utils.add_project("Project 1", "URL 1", "Description 1")
        overview = projects.utils.get_active_projects_overview()

        assert overview == [{
            "id": 1,
            "name": "Project 1",
            "url": "URL 1"
        }]

    def test_active_projects_overview_two(self):
        projects.utils.add_project("Project 1", "URL 1", "Description 1")
        time.sleep(0.1)
        projects.utils.add_project("Project 2", "URL 2", "Description 1")
        overview = projects.utils.get_active_projects_overview()

        assert overview == [{
            "id": 1,
            "name": "Project 1",
            "url": "URL 1"
        },
        {
            "id": 2,
            "name": "Project 2",
            "url": "URL 2"
        }]

    def test_active_projects_overview_deactivated(self):
        projects.utils.add_project("Project 1", "URL 1", "Description 1")
        time.sleep(0.1)
        projects.utils.add_project("Project 2", "URL 2", "Description 1")

        projects.utils.deactivate_project(1)
        overview = projects.utils.get_active_projects_overview()

        assert overview == [{
            "id": 2,
            "name": "Project 2",
            "url": "URL 2"
        }]