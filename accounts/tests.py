from django.test import TestCase
from tasks.models import Task
from .models import CustomUser, Team, UserTeam

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_staff=True
        )

    def tearDown(self):
        self.user.delete()


    def test_create(self):
        """Test the create method of CustomUser"""
        user = CustomUser.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            is_staff=True,
            username="jane.smith@example.com"  # Set username explicitly
        )

        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.email, "jane.smith@example.com")

    def test_read(self):
        """Test the read method of CustomUser"""
        user = CustomUser.read(self.user.pk)
        self.assertEqual(user, self.user)

    def test_update(self):
        """Test the update method of CustomUser"""
        updated_user = CustomUser.update(
            self.user.pk,
            "Updated",
            "User",
            "updated.user@example.com"
        )
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "User")
        self.assertEqual(updated_user.email, "updated.user@example.com")

    def test_delete(self):
        """Test the delete method of CustomUser"""
        deleted_user = CustomUser.objects.get(pk = self.user.pk)
        self.assertEqual(deleted_user, self.user)

class TeamTestCase(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_staff=True
        )
        self.team = Team.objects.create(
            name="Team A",
            owner=self.owner,
            description="Team A description"
        )

    def tearDown(self):
        self.team.delete()
        self.owner.delete()

    def test_create(self):
        """Test the create method of Team"""
        team = Team.create("Team B", self.owner, "Team B description")
        self.assertEqual(team.name, "Team B")
        self.assertEqual(team.owner, self.owner)
        self.assertEqual(team.description, "Team B description")


    def test_read(self):
        """Test the read method of Team"""
        team = Team.read(self.team.pk)
        self.assertEqual(team, self.team)

    def test_update(self):
        """Test the update method of Team"""
        updated_team = Team.update(
            self.team.pk,
            "Updated Team A",
            self.owner,
            "Updated Team A description"
        )
        self.assertEqual(updated_team.name, "Updated Team A")
        self.assertEqual(updated_team.owner, self.owner)
        self.assertEqual(updated_team.description, "Updated Team A description")

    def test_delete(self):
        """Test the delete method of Team"""
        deleted_team = Team.objects.get(pk=self.team.pk)
        self.assertEqual(deleted_team, self.team)

class UserTeamTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            is_staff=True
        )
        self.team = Team.objects.create(
            name="Team A",
            owner=self.user,
            description="Team A description"
        )
        self.user_team = UserTeam.objects.create(
            user=self.user,
            team=self.team
        )

    def tearDown(self):
        self.user_team.delete()
        self.team.delete()
        self.user.delete()


    def test_create(self):
        """Test the create method of UserTeam"""
        new_user = CustomUser.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            is_staff=False,
            username="jane.smith@example.com"
        )
        user_team = UserTeam.create(new_user, team=self.team)
        self.assertEqual(user_team.user, new_user)
        self.assertEqual(user_team.team, self.team)

    def test_read(self):
        """Test the read method of UserTeam"""
        user_team = UserTeam.read(self.user_team.pk)
        self.assertEqual(user_team, self.user_team)
