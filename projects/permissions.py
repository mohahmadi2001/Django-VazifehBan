from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from accounts.models import Team

class IsTeamMember(BasePermission):
    def has_permission(self, request, view):
        team_pk = request.data.get('team')
        team = get_object_or_404(Team, pk=team_pk)
        return team.is_member(request.user)


class IsTeamOwner(BasePermission):
    def has_permission(self, request, view):
        team_pk = request.data.get('team')
        team = get_object_or_404(Team, pk=team_pk)
        return team.is_owner(request.user)
    
class IsWorkspaceOwner(BasePermission):
    """
    Checks if the user is the owner of the workspace.
    """

    def has_permission(self, request, view):
        workspace = view.get_workspace()
        return workspace.team.is_owner(request.user)