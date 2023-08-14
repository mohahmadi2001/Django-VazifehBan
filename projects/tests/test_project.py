import unittest
from django.test import TestCase
from datetime import datetime, timedelta
from models import Project, WorkSpace

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


if __name__ == '__main__':
    unittest.main()