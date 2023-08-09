from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    teams = models.ManyToManyField('Team', through='UserTeam')


    # Extra fields for specific users and superusers
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Custom functionality for specific users and superusers
    def is_admin(self):
        return self.is_superuser

    def is_staff_or_admin(self):
        return self.is_staff or self.is_superuser
    
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, through='UserTeam')
    description = models.TextField()

class UserTeam(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')
