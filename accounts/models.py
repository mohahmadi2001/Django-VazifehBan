from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class User(AbstractUser):
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email"), unique=True)
    teams = models.ManyToManyField("Team", verbose_name=_("Teams"), through='UserTeam')
    is_staff = models.BooleanField(_("First Name"), default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    users = models.ManyToManyField("User", verbose_name=_("Users"), through='UserTeam')
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name


class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_owner = models.BooleanField(verbose_name=_("Is Owner"), default=False)

    class Meta:
        verbose_name = _("User Team")
        verbose_name_plural = _("User Teams")

    def __str__(self):
        return self.id
