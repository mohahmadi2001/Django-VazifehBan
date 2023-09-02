from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework import permissions

from accounts.models import Team
from projects.models import Project, Sprint

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
        # Check if the user is the owner of the team associated with the workspace.
        workspace = view.get_object()
        user = request.user
        team = workspace.team

        return team.is_owner(user)
    
    
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
        workspace = view.get_object()
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

class IsProjectOwner(BasePermission):
    """
    Custom permission to check if a user is the owner of the project.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the project ID from the URL kwargs
        project_pk = view.kwargs.get('project_pk')

        # Get the project object
        project = get_object_or_404(Project, pk=project_pk)

        # Check if the user is the owner of the project
        return project.team.is_owner(request.user)
    
class IsTeamMemberOrOwner(BasePermission):
    """
    Custom permission to allow only team members or owners to perform actions.
    """

    def has_permission(self, request, view):
        team_id = view.kwargs.get('team_pk')  # Assuming the team ID is passed as a URL parameter
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return False

        return team.is_member(request.user) or team.is_owner(request.user)
    
    
    
class IsSprintOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        sprint_id = view.kwargs.get('sprint_id')
        try:
            sprint = Sprint.objects.get(id=sprint_id)
            project = sprint.project

            # Check if the project has a team
            if project.team:
                return request.user == project.team.owner
            else:
                return request.user == project.owner
        except Sprint.DoesNotExist:
            return False