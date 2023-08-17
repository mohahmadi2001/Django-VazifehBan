from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

import logging

from accounts.models import Team
from .serializers import WorkSpaceSerializer
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