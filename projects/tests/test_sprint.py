import unittest
from django.test import TestCase
from datetime import datetime, timedelta
from models import Sprint, Project, WorkSpace

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

    

if __name__ == '__main__':
    unittest.main()