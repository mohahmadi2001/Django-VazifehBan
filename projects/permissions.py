from rest_framework.permissions import BasePermission
from rest_framework import permissions

from accounts.models import Team
from projects.models import Project

class IsTeamMember(BasePermission):
    """
    Permission to check if a user is a member of the team associated with the view.

    Args:
        request: The HTTP request.
        view: The view where the permission is checked.

    Returns:
        bool: True if the user is a member of the team, False otherwise.
    """
    def has_permission(self, request, view):
        team = view.get_team()
        return team.is_member(request.user)

class IsTeamOwner(BasePermission):
    """
    Permission to check if a user is the owner of the team associated with the view.

    Args:
        request: The HTTP request.
        view: The view where the permission is checked.

    Returns:
        bool: True if the user is the owner of the team, False otherwise.
    """
    def has_permission(self, request, view):
        team = view.get_team()
        return team.is_owner(request.user)

class IsWorkspaceOwner(BasePermission):
    """
    Permission to check if a user is the owner of the workspace associated with the view.

    Args:
        request: The HTTP request.
        view: The view where the permission is checked.

    Returns:
        bool: True if the user is the owner of the workspace, False otherwise.
    """
    def has_permission(self, request, view):
        workspace = view.get_workspace()
        return workspace.team.is_owner(request.user)

class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to check if a user is a member of the project associated with the view.

    Args:
        request: The HTTP request.
        view: The view where the permission is checked.

    Returns:
        bool: True if the user is a member of the project, False otherwise.
    """
    def has_permission(self, request, view):
        project = view.get_project()
        return project.team.members.filter(id=request.user.id).exists()
