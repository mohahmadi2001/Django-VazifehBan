from django.contrib import admin
from .models import CustomUser, Team, UserTeam


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'description')
    filter_horizontal = ('members',)  
    raw_id_fields = ('owner',) 

@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ('user', 'team')  