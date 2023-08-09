from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    teams = models.ManyToManyField('Team', through='UserTeam')


    # Extra fields for specific users and superusers
    is_staff = models.BooleanField(default=False)
    

    def is_staff(self):
        return self.is_staff 
    
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, through='UserTeam')
    description = models.TextField()

class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')
