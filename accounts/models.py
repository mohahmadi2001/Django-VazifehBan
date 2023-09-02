from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from core.models import SoftDeleteModel


class CustomUser(SoftDeleteModel, AbstractUser):
    teams = models.ManyToManyField('Team', through='UserTeam', related_name='team_members', verbose_name=_("Teams"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_staff_status(self):
        return self.is_staff

    def __str__(self):
        return f"{self.username}"

    def has_permission(self, permission_codename):
        """
        Returns True if the user has the specified permission.

        Args:
            permission_codename: The code name of the permission.

        Returns:
            True if the user has the permission, False otherwise.
        """
        if permission_codename == 'workspaces.view':
            return True
        return super().has_permission(permission_codename)

    @classmethod
    def create(cls, first_name, last_name, email):
        """Creates a new user.

        Args:
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            email (str): Email address of the user.

        Returns:
            CustomUser: The newly created user object.
        """

        return cls.objects.create(first_name=first_name, last_name=last_name, email=email)

    @classmethod
    def read(cls, pk):
        """Retrieves the user from the database.

        Args:
            pk (int): Primary key of the user.

        Returns:
            CustomUser: The user object.
        """
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    @classmethod
    def update(cls, pk, new_first_name, new_last_name, new_email):
        """Updates the user in the database.

        Args:
            pk (int): Primary key of the user.
            new_first_name (str): New first name of the user.
            new_last_name (str): New last name of the user.
            new_email (str): New email address of the user.

        Returns:
            CustomUser: The updated user object.
        """

        user = cls.objects.get(pk=pk)
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.save()
        return user


class Team(SoftDeleteModel, models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    members = models.ManyToManyField(CustomUser, through='UserTeam', related_name="teams_as_member",
                                     verbose_name=_("Users"))
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_teams")
    description = models.TextField(verbose_name=_("Description"))
    title = models.CharField(max_length=255, default=' Title')

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name

    def is_member(self, user):
        """
        Check if a user is a member of this team.

        Args:
            user (User): The user to check for membership.

        Returns:
            bool: True if the user is a member of this team, False otherwise.
        """
        return self.members.filter(id=user.id).exists()

    def is_owner(self, user):
        """Check if a user is the owner of the team."""
        return self.owner == user

    @classmethod
    def create(cls, name, owner, description):
        """Creates a new team.

        Args:
            name (str): Name of the team.
            owner (CustomUser): Owner of the team.
            description (str): Description of the team.

        Returns:
            Team: The newly created team object.
        """

        return cls.objects.create(name=name, owner=owner, description=description)

    @classmethod
    def read(cls, pk):
        """Retrieves the team from the database.

        Args:
            pk (int): Primary key of the team.

        Returns:
            Team: The team object.

        Raises:
            Team.DoesNotExist: If the team with the given primary key does not exist.
        """

        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise Team.DoesNotExist(f"Team with pk={pk} does not exist.")

    @classmethod
    def update(cls, pk, new_name, new_owner, new_description):
        """Updates the team in the database.

        Args:
            pk (int): Primary key of the team.
            new_name (str): New name of the team.
            new_owner (CustomUser): New owner of the team.
            new_description (str): New description of the team.

        Returns:
            Team: The updated team object.

        Raises:
            Team.DoesNotExist: If the team with the given primary key does not exist.
        """

        try:
            team = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise Team.DoesNotExist(f"Team with pk={pk} does not exist.")

        team.name = new_name
        team.owner = new_owner
        team.description = new_description
        team.save()
        return team


class UserTeam(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_users")

    class Meta:
        verbose_name = _("User Team")
        verbose_name_plural = _("User Teams")

    def __str__(self):
        return f"UserTeam - user: {self.user}, team: {self.team}"

    @classmethod
    def create(cls, user, team):
        """Creates a new user-team relationship.

        Args:
            user (CustomUser): User object.
            team (Team): Team object.

        Returns:
            UserTeam: The newly created user-team relationship object.
        """

        return cls.objects.create(user=user, team=team)

    @classmethod
    def read(cls, pk):
        """Retrieves the user-team relationship from the database.

        Args:
            pk (int): Primary key of the user-team relationship.

        Returns:
            UserTeam: The user-team relationship object.
        """

        return cls.objects.get(pk=pk)
