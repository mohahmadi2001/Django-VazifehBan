import unittest
from django.test import TestCase
from datetime import datetime, timedelta
from projects.models import Sprint, Project, WorkSpace
from accounts.models import Team

class ProjectTestCase(TestCase):
    def setUp(self):
        self.workspace = WorkSpace.objects.create(title="Test Workspace")
        self.project_data = {
            "title": "Test Project",
            "description": "This is a test project description.",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=7),
            "deadline": datetime.now() + timedelta(days=14),
            "workspace": self.workspace,
        }

    def test_create_project(self):
        project = Project.objects.create_project(**self.project_data)
        self.assertEqual(project.title, self.project_data["title"])
        self.assertEqual(project.description, self.project_data["description"])
 

    def test_get_project_info(self):
        project = Project.objects.create_project(**self.project_data)
        project_info = project.get_project_info()
        self.assertEqual(project_info["title"], self.project_data["title"])
        self.assertEqual(project_info["description"], self.project_data["description"])


    def test_edit_project(self):
        project = Project.objects.create_project(**self.project_data)
        new_title = "Updated Project Title"
        project.edit_project(title=new_title)
        project.refresh_from_db()
        self.assertEqual(project.title, new_title)


class SprintTestCase(TestCase):
    def setUp(self):
        self.workspace = WorkSpace.objects.create(title="Test Workspace")
        self.project = Project.objects.create_project(
            title="Test Project",
            description="This is a test project description.",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7),
            deadline=datetime.now() + timedelta(days=14),
            workspace=self.workspace,
        )
        self.sprint_data = {
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=14),
            "project": self.project,
        }

    def test_create_sprint(self):
        sprint = Sprint.objects.create_sprint(**self.sprint_data)
        self.assertEqual(sprint.start_date, self.sprint_data["start_date"])
        self.assertEqual(sprint.end_date, self.sprint_data["end_date"])
        

    def test_get_sprint_info(self):
        sprint = Sprint.objects.create_sprint(**self.sprint_data)
        sprint_info = sprint.get_sprint_info()
        self.assertEqual(sprint_info["start_date"], self.sprint_data["start_date"])
        self.assertEqual(sprint_info["end_date"], self.sprint_data["end_date"])
        

    def test_edit_sprint(self):
        sprint = Sprint.objects.create_sprint(**self.sprint_data)
        new_start_date = datetime.now() + timedelta(days=7)
        sprint.edit_sprint(start_date=new_start_date)
        sprint.refresh_from_db()
        self.assertEqual(sprint.start_date, new_start_date)


class WorkSpaceTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.workspace = WorkSpace.objects.create(title="Test Workspace", team=self.team)
    
    def test_create_workspace(self):
        title = "New Workspace"
        team = self.team
        workspace = WorkSpace.create_workspace(title, team)
        
        self.assertEqual(workspace.title, title)
        self.assertEqual(workspace.team, team)
    
    def test_get_workspace_information(self):
        info = self.workspace.get_workspace_information()
        
        self.assertEqual(info['title'], self.workspace.title)
        self.assertEqual(info['team'], self.workspace.team.name)
    
    def test_edit_workspace_title(self):
        new_title = "Updated Workspace Title"
        self.workspace.edit_workspace(new_title)
        
        self.assertEqual(self.workspace.title, new_title)
    
    def test_edit_workspace_team(self):
        new_team = Team.objects.create(name="New Test Team")
        self.workspace.edit_workspace(self.workspace.title, new_team)
        
        self.assertEqual(self.workspace.team, new_team)


if __name__ == '__main__':
    unittest.main()