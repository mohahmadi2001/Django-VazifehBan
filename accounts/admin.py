from django.contrib import admin
from .models import CustomUser, Team, UserTeam


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    pass

