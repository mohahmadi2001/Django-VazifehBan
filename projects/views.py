from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

import logging

from accounts.models import Team
from projects.models import WorkSpace
from .serializers import WorkSpaceDetailWithProjectsAndTeamSerializer, WorkSpaceSerializer
from .permissions import IsTeamMember, IsTeamOwner

class WorkSpaceCreateView(CreateAPIView):
    """
    View for creating a WorkSpace for a particular team with owner's permission.

    Attributes:
        serializer_class (class): The serializer class to use for creating a workspace.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, IsTeamMember, IsTeamOwner]

    def create(self, request, *args, **kwargs) -> Response:
        """
        Creates a new WorkSpace.

        Args:
            request (HttpRequest): The HTTP request.
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
            A response object.

        Raises:
            PermissionDenied: If the user is not the owner of the team.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Workspace created successfully",
            "workspace": serializer.data
        }
        return Response(response_data, status=201, headers=headers)

    def perform_create(self, serializer) :
        """
        Performs the create operation.

        Args:
            serializer (Serializer): The serializer instance.

        Returns:
            The newly created object.

        Raises:
            PermissionDenied: If the user is not the owner of the team.
        """
        team_pk = serializer.validated_data.get('team')
        team = get_object_or_404(Team, pk=team_pk)
        
        if not team.exists():
            raise PermissionDenied("The team does not exist.")
        
        if not team.is_member(self.request.user):
            raise PermissionDenied("You must be a member of the team to create a workspace.")
        
        return serializer.save(team=team)
    
    def log_workspace_creation(self, workspace):
        """
        Logs the creation of a workspace.

        Args:
            workspace: The newly created workspace object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace created: {workspace.title}, Team: {workspace.team.name}")


class WorkSpaceEditView(RetrieveUpdateAPIView):
    """
    View for editing workspace information by user permission.

    **Arguments:**
        team_pk (int): The ID of the team that the workspace belongs to.
        workspace_pk (int): The ID of the workspace to be edited.

    **Permissions:**
        IsAuthenticated: The user must be authenticated.
        IsTeamMember: The user must be a member of the team that the workspace belongs to.

    **Returns:**
        A response object with the updated workspace information.

    **Raises:**
        PermissionDenied: If the user does not have permission to edit the workspace.

    """

    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, IsTeamMember]

    def get_queryset(self):
        """
        Gets the queryset for the workspaces that the user can edit.

        **Returns:**
            The queryset for the workspaces that the user can edit.
        """
        team_pk = self.kwargs.get('team_pk')
        workspace_pk = self.kwargs.get('workspace_pk')
        return WorkSpace.objects.filter(team__pk=team_pk, pk=workspace_pk)

    def update(self, request, *args, **kwargs):
        """
        Updates the workspace information.

        **Arguments:**
            request (django.http.HttpRequest): The HTTP request.

        **Raises:**
            PermissionDenied: If the user does not have permission to edit the workspace.

        **Returns:**
            A response object with the updated workspace information.
        """
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not workspace.team.is_member(request.user):
            raise PermissionDenied("You are not a member of this team.")

        self.perform_update(serializer)
        return Response(serializer.data)

    def log_workspace_update(self, workspace):
        """
        Logs the editing of a workspace.

        Args:
            workspace: The newly edited workspace object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace updated: {workspace.title}, Team: {workspace.team.name}")


class WorkSpaceDetailView(RetrieveAPIView):
    """
    View for showing workspace information along with projects and team information.

    **Arguments:**
        workspace_pk (int): The ID of the workspace to be displayed.

    **Permissions:**
        IsAuthenticated: The user must be authenticated.
        IsTeamOwner: The user must be the owner of the workspace.

    **Returns:**
        A response object with the workspace information, projects, and team information.

    **Raises:**
        PermissionDenied: If the user does not have permission to view the workspace.

    """

    serializer_class = WorkSpaceDetailWithProjectsAndTeamSerializer
    permission_classes = [IsAuthenticated, IsTeamOwner]

    def get_queryset(self):
        """
        Gets the queryset for the workspaces that the user can view.

        **Returns:**
            The queryset for the workspaces that the user can view.
        """
        workspace_pk = self.kwargs.get('workspace_pk')
        return WorkSpace.objects.filter(
            team__members__in=[self.request.user]
        ).filter(pk=workspace_pk)

    def get(self, request, *args, **kwargs):
        """
        Retrieve the workspace information.

        **Arguments:**
            request (django.http.HttpRequest): The HTTP request.

        **Raises:**
            PermissionDenied: If the user does not have permission to view the workspace.

        **Returns:**
            A response object with the workspace information, projects, and team information.
        """
        workspace = self.get_object()
        serializer = self.get_serializer(workspace)
        return Response(serializer.data)