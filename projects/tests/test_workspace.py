import unittest
from django.test import TestCase
from models import WorkSpace
from accounts.models import Team

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