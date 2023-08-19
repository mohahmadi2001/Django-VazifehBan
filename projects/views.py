from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

import logging

from accounts.models import Team
from projects.models import Project, Sprint, WorkSpace
from .serializers import ProjectDetailWithSprintsSerializer, ProjectSerializer, SprintDetailSerializer, SprintSerializer, WorkSpaceDetailWithProjectsAndTeamSerializer, WorkSpaceSerializer
from .permissions import IsProjectMember, IsProjectOwner, IsTeamMember, IsTeamOwner, IsWorkspaceOwner

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

        self.log_workspace_retrieval(workspace)


        return Response(serializer.data)
    
    
    def log_workspace_retrieval(self, workspace):
        """
        Logs the retrieval of workspace information.

        Args:
            workspace: The workspace object being retrieved.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace retrieved: ID {workspace.id}, Team: {workspace.team.name}")
    

class WorkSpaceDeleteView(DestroyAPIView):
    """
    View for deleting a workspace by the owner.

    Attributes:
        queryset (QuerySet): The queryset for retrieving the workspace.
        serializer_class (class): The serializer class to use for deleting the workspace.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, IsTeamOwner]

    def destroy(self, request, *args, **kwargs):
        workspace = self.get_object()

        if not workspace.team.is_owner(request.user):
            raise PermissionDenied("You are not the owner of this workspace.")

        self.log_workspace_deletion(workspace)

        workspace.soft_delete()
        return Response({"message": "Workspace deleted successfully"}, status=200)
    
    def log_workspace_deletion(self, workspace):
        """
        Logs the deletion of a workspace.

        Args:
            workspace: The workspace object being deleted.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace deleted: ID {workspace.id}, Team: {workspace.team.name}")

    

class ProjectCreateView(CreateAPIView):
    """
    View for creating a project by workspace owner permission.

    Attributes:
        serializer_class (class): The serializer class to use for creating a project.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwner]

    def create(self, request, *args, **kwargs):
        """
        Creates a new project within a workspace.

        Args:
            request: The HTTP request.
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
            A response object.
        """
        workspace = self.get_workspace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.perform_create(serializer, workspace)
        headers = self.get_success_headers(serializer.data)
        
        response_data = {
            "message": "Project created successfully",
            "project": serializer.data
        }
        
        self.log_project_creation(project)

        return Response(response_data, status=201, headers=headers)

    def get_workspace(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        workspace = get_object_or_404(WorkSpace, pk=workspace_pk)
        return workspace

    def perform_create(self, serializer, workspace):
        """
        Performs the create operation for the project.

        Args:
            serializer: The serializer instance.
            workspace: The workspace associated with the project.

        Returns:
            The newly created project object.
        """
        return serializer.save(workspace=workspace)
    
    def log_project_creation(self, project):
        """
        Logs the creation of a project.

        Args:
            project: The newly created project object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project created: {project.title}, Workspace: {project.workspace.title}")
    

class SprintCreateView(CreateAPIView):
    """
    View for creating a sprint by team owner permission.

    Attributes:
        serializer_class (class): The serializer class to use for creating a sprint.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsTeamOwner]

    def create(self, request, *args, **kwargs):
        """
        Creates a new sprint.

        Args:
            request (HttpRequest): The HTTP request.
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
            A response object.

        Raises:
            PermissionDenied: If the user is not the owner of the team.
        """
        project = self.get_project_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sprint = self.perform_create(serializer, project)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Sprint created successfully",
            "sprint": serializer.data
        }
        return Response(response_data, status=201, headers=headers)

    def get_project_object(self):
        """
        Retrieves the project object based on URL parameters.

        Returns:
            Project: The project object.
        """
        project_id = self.kwargs.get('project_id')
        return get_object_or_404(Project, pk=project_id)

    def perform_create(self, serializer, project):
        """
        Performs the create operation.

        Args:
            serializer (Serializer): The serializer instance.
            project (Project): The project associated with the sprint.

        Returns:
            The newly created sprint object.

        Raises:
            PermissionDenied: If the user is not the owner of the team.
        """
        sprint = serializer.save(project=project)
        
        # Log the creation of a sprint
        self.log_sprint_creation(sprint)
        
        return sprint

    def log_sprint_creation(self, sprint):
        """
        Logs the creation of a sprint.

        Args:
            sprint: The newly created sprint object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Sprint created: {sprint.id}, Project: {sprint.project.title}")


class ProjectDetailView(RetrieveAPIView):
    """
    View for showing project information along with sprints by member permission.

    **Arguments:**
        project_pk (int): The ID of the project to be displayed.

    **Permissions:**
        IsAuthenticated: The user must be authenticated.
        IsProjectMember: The user must be a member of the project.

    **Returns:**
        A response object with the project information and a list of sprints.

    **Raises:**
        PermissionDenied: If the user does not have permission to view the project.
    """

    serializer_class = ProjectDetailWithSprintsSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        """
        Gets the queryset for the projects that the user can view.

        **Returns:**
            The queryset for the projects that the user can view.
        """
        project_pk = self.kwargs.get('project_pk')
        return Project.objects.filter(
            team__members__in=[self.request.user]
        ).filter(pk=project_pk)

    def get(self, request, *args, **kwargs):
        """
        Retrieve the project information along with sprints.

        **Arguments:**
            request (django.http.HttpRequest): The HTTP request.

        **Raises:**
            PermissionDenied: If the user does not have permission to view the project.

        **Returns:**
            A response object with the project information and a list of sprints.
        """
        project = self.get_object()
        serializer = self.get_serializer(project)
        self.log_project_view(project)

        return Response(serializer.data)
    
    def log_project_view(self, project):
        """
        Log the viewing of a project.

        Args:
            project: The viewed project object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project viewed: {project.title}, Team: {project.team.name}")

    
class ProjectEditView(RetrieveUpdateAPIView):
    """
    View for editing project information by owner permission.

    Attributes:
        serializer_class (class): The serializer class to use for editing project information.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        """
        Gets the queryset for the projects that the user can edit.

        Returns:
            The queryset for the projects that the user can edit.
        """
        return Project.objects.filter(team__members=self.request.user)

    def get_object(self):
        """
        Retrieves the project object.

        Returns:
            The project object to edit.
        """
        project_pk = self.kwargs.get('project_pk')
        return get_object_or_404(self.get_queryset(), pk=project_pk)

    def update(self, request, *args, **kwargs):
        """
        Updates the project information.

        Args:
            request: The HTTP request.
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
            A response object.

        Raises:
            PermissionDenied: If the user is not the owner of the project.
        """
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if not project.team.is_owner(request.user):
            raise PermissionDenied("You are not the owner of this project.")

        self.log_project_edit(project)

        self.perform_update(serializer)
        return Response(serializer.data)
    
    def log_project_edit(self, project):
        """
        Log the editing of a project.

        Args:
            project: The edited project object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project edited: {project.title}, Team: {project.team.name}")


class ProjectDeleteView(DestroyAPIView):
    """
    View for deleting a project by the owner.

    Attributes:
        queryset (QuerySet): The queryset for retrieving the project.
        serializer_class (class): The serializer class to use for deleting the project.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if not project.workspace.is_owner(request.user):
            raise PermissionDenied("You are not the owner of this project's workspace.")

        # Log the deletion of the project
        self.log_project_deletion(project)
        
        project.soft_delete()
        return Response({"message": "Project deleted successfully"}, status=200)
    
    def log_project_deletion(self, project):
        """
        Logs the deletion of a project.

        Args:
            project: The project object being deleted.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project deleted: ID {project.id}, Workspace: {project.workspace.title}")

class SprintEditView(RetrieveUpdateAPIView):
    """
    View for editing a sprint by the owner.

    Attributes:
        serializer_class (class): The serializer class to use for editing the sprint.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Gets the queryset for retrieving the sprint.

        **Returns:**
            The queryset for retrieving the sprint.
        """
        sprint_id = self.kwargs.get('sprint_id')
        return Sprint.objects.filter(pk=sprint_id)

    def update(self, request, *args, **kwargs):
        sprint = self.get_object()

        if not sprint.project.workspace.team.is_owner(request.user):
            raise PermissionDenied("You are not the owner of this sprint's team.")

        serializer = self.get_serializer(sprint, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # You can add logging here if needed
        self.log_sprint_update(sprint)

        return Response(serializer.data)

    def log_sprint_update(self, sprint):
        """
        Logs the editing of a sprint.

        Args:
            sprint: The newly edited sprint object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Sprint updated: {sprint.title}, Project: {sprint.project.title}")


class SprintDeleteView(DestroyAPIView):
    """
    View for deleting a sprint by owner permission.

    Attributes:
        queryset (QuerySet): The queryset for retrieving the sprint.
        serializer_class (class): The serializer class to use for deleting the sprint.
        permission_classes (list): The list of permission classes required for accessing this view.
    """
    queryset = Sprint.objects.all()
    serializer_class = SprintDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def destroy(self, request, *args, **kwargs):
        sprint = self.get_object()

        # Check if the user has permission to delete this sprint
        if not sprint.project.workspace.team.is_owner(request.user):
            raise PermissionDenied("You are not the owner of this sprint.")

        # Add a confirmation step
        if not request.user.confirm_delete(sprint):
            return Response({"message": "Deletion cancelled"}, status=400)

        # Perform soft delete on the sprint
        sprint.soft_delete()

        # Log sprint deletion
        self.log_sprint_deletion(sprint)

        return Response({"message": "Sprint deleted successfully"}, status=200)

    def log_sprint_deletion(self, sprint):
        """
        Logs the deletion of a sprint.

        Args:
            sprint: The deleted sprint object.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Sprint deleted: {sprint.title}, Team: {sprint.project.workspace.team.name}")
