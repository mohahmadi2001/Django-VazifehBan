  
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import Team
from .models import Project, Sprint, WorkSpace
from .serializers import ProjectSerializer, SprintSerializer, TeamSerializer, WorkSpaceSerializer
from .permissions import IsProjectMember, IsSprintOwner, IsTeamMember, IsTeamMemberOrOwner, IsTeamOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
import logging
from rest_framework.permissions import AllowAny
logger = logging.getLogger(__name__)




class WorkSpaceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, retrieving, updating, and deleting workspaces.

    This ViewSet allows you to perform CRUD operations on workspace objects. Workspaces
    are associated with projects and have various permissions depending on the user's role.

    Attributes:
        serializer_class (class): The serializer class for serializing workspace objects.
        lookup_field (str): The field to use when looking up workspace objects.
        logger (Logger): The logger instance for logging workspace-related actions.
    """

    serializer_class = WorkSpaceSerializer
    # permission_classes = [IsTeamMemberOrOwner]
    lookup_field = 'pk'  
    logger = logging.getLogger(__name__)

    def get_queryset(self):
        """
        Get the queryset for the workspaces based on user role/permissions.

        Returns:
            QuerySet: A queryset of workspace objects filtered based on user permissions.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                # Superuser can see all workspaces
                return WorkSpace.objects.all()
            elif user.has_perm('workspaces.view_workspace'):
                # Users with permission to view workspaces
                return WorkSpace.objects.all()
            elif user.has_perm('workspaces.change_workspace'):
                # Users with permission to change workspaces (editors)
                return WorkSpace.objects.filter(editors=user)
            elif user.has_perm('workspaces.add_workspace'):
                # Users with permission to add workspaces (contributors)
                return WorkSpace.objects.filter(contributors=user)
        # If the user doesn't have any relevant permissions, return an empty queryset or handle as needed
        return WorkSpace.objects.none()
    
    def create(self, request, *args, **kwargs):
        """
        Create a new workspace within a project.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the result of the workspace creation.
        """
        user = self.request.user
        project = self.get_project()
        if not user.has_perm('workspaces.add_workspace'):
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set the 'team' field of the workspace before saving
        workspace = serializer.save(project=project, team=project.team)
        
        response_data = {
            "message": "Workspace created successfully",
            "workspace": serializer.data
        }
        self.log_workspace_creation(workspace)
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve workspace information.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response containing the serialized workspace data.
        """
        workspace = self.get_object()
        serializer = self.get_serializer(workspace)
        self.log_workspace_view(workspace)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update workspace information.
        """
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not workspace.project.editors.filter(id=request.user.id).exists():
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        self.log_workspace_edit(workspace)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a workspace.
        """
        workspace = self.get_object()
        if not workspace.project.editors.filter(id=request.user.id).exists():
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        self.log_workspace_deletion(workspace)
        workspace.soft_delete()
        return Response({"message": "Workspace deleted successfully"}, status=status.HTTP_200_OK)

    def get_project(self):
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)
        return project

    def perform_create(self, serializer, project):
        """
        Perform the create operation for the workspace.
        """
        return serializer.save(project=project)
    
    

    def log_workspace_creation(self, workspace):
        """
        Log the creation of a workspace.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace created: {workspace.title}, Project: {workspace.project.title}")

    def log_workspace_view(self, workspace):
        project_title = ""
        if hasattr(workspace, "project"):
            project_title = workspace.project.title
        
        logger.info("Workspace viewed: %s, Project: %s", workspace.title, project_title)

    def log_workspace_edit(self, workspace):
        """
        Log the editing of a workspace.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace edited: {workspace.title}, Project: {workspace.project.title}")

    def log_workspace_deletion(self, workspace):
        """
        Log the deletion of a workspace.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Workspace deleted: ID {workspace.id}, Project: {workspace.project.title}")


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, retrieving, updating, and deleting projects.

    This ViewSet allows you to perform CRUD operations on project objects. Projects
    are associated with workspaces and have various permissions depending on the user's role.

    Attributes:
        serializer_class (class): The serializer class for serializing project objects.
    """

    serializer_class = ProjectSerializer
    # permission_classes = [IsProjectMember, IsTeamMemberOrOwner]

    def get_queryset(self):
        """
        Get the queryset for the projects based on user role/permissions.

        Returns:
            QuerySet: A queryset of project objects filtered based on user permissions.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                # Superuser can see all projects
                return Project.objects.all()
            elif user.has_perm('projects.view_project'):
                # Users with permission to view projects
                return Project.objects.all()
            elif user.has_perm('projects.change_project'):
                # Users with permission to change projects (editors)
                return Project.objects.filter(editors=user)
            elif user.has_perm('projects.add_project'):
                # Users with permission to add projects (contributors)
                return Project.objects.filter(contributors=user)
        # If the user doesn't have any relevant permissions, return an empty queryset or handle as needed
        return Project.objects.none()
    
    def create(self, request, *args, **kwargs):
        """
        Create a new project within a workspace.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the result of the project creation.
        """
        user = self.request.user
        workspace = self.get_workspace()
        if not user.has_perm('projects.add_project'):
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = self.perform_create(serializer, workspace)
        response_data = {
            "message": "Project created successfully",
            "project": serializer.data
        }
        self.log_project_creation(project)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve project information.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response containing the serialized project data.
        """
        project = self.get_object()
        serializer = self.get_serializer(project)
        self.log_project_view(project)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        """
        Update project information.
        """
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not project.team.is_owner(request.user):
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        self.log_project_edit(project)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a project.
        """
        project = self.get_object()
        if not project.workspace.is_owner(request.user):
            return Response({"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        self.log_project_deletion(project)
        project.soft_delete()
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_200_OK)

    def get_workspace(self):
        workspace_pk = self.kwargs.get('workspace_pk')
        workspace = get_object_or_404(WorkSpace, pk=workspace_pk)
        return workspace

    def perform_create(self, serializer, workspace):
        """
        Perform the create operation for the project.
        """
        return serializer.save(workspace=workspace)

    def log_project_creation(self, project):
        """
        Log the creation of a project.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project created: {project.title}, Workspace: {project.workspace.title}")

    def log_project_view(self, project):
        """
        Log the viewing of a project.
        """
        logger = logging.getLogger(__name__)
        if project.team:
            logger.info(f"Project viewed: {project.title}, Team: {project.team.name}")
        else:
            logger.info(f"Project viewed: {project.title}, No associated team")


    def log_project_edit(self, project):
        """
        Log the editing of a project.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project edited: {project.title}, Team: {project.team.name}")

    def log_project_deletion(self, project):
        """
        Log the deletion of a project.
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Project deleted: ID {project.id}, Workspace: {project.workspace.title}")
        

class SprintViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, retrieving, updating, and deleting sprints.

    This ViewSet allows you to perform CRUD operations on sprint objects. Sprints are associated with projects
    and have various permissions depending on the user's role.

    Attributes:
        queryset (QuerySet): The queryset for retrieving sprints.
        serializer_class (class): The serializer class for serializing sprint objects.
        permission_classes (list): The list of permission classes for controlling access to sprints.
        lookup_field (str): The lookup field used to retrieve sprints by their ID.
    """
    
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsSprintOwner, IsTeamMemberOrOwner]
    lookup_field = 'id'
   
    def get_queryset(self):
        """
        Get the queryset for sprints based on user role/permissions.

        Returns:
            QuerySet: A queryset of sprint objects filtered based on user permissions.
        """
        user = self.request.user
        if user.is_authenticated and user.has_perm('projects.add_sprint'):
            return Sprint.objects.all()
        return Sprint.objects.none()
    
    
    def create(self, request, *args, **kwargs):
        """
        Create a new sprint within a project.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating the result of the sprint creation.
        """
        project = self.get_project()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check ownership
        if project.team:
            if request.user != project.team.owner:
                return Response({'message': 'You do not have permission to create a sprint in this project.'}, 
                                status=status.HTTP_403_FORBIDDEN)
        elif request.user != project.owner:
            return Response({'message': 'You do not have permission to create a sprint in this project.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        sprint = self.perform_create(serializer, project)
        response_data = {
            "message": "Sprint created successfully",
            "sprint": serializer.data
        }
        self.log_sprint_creation(sprint)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve sprint information.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response containing the serialized sprint data.
        """
        sprint = self.get_object()
        
        # Check ownership
        project = sprint.project
        if project.team:
            if request.user != project.team.owner:
                return Response({'message': 'You do not have permission to retrieve this sprint.'}, 
                                status=status.HTTP_403_FORBIDDEN)
        elif request.user != project.owner:
            return Response({'message': 'You do not have permission to retrieve this sprint.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(sprint)
        self.log_sprint_retrieval(sprint)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a sprint.
        """
        sprint = self.get_object()
        
        # Check ownership
        project = sprint.project
        if project.team:
            if request.user != project.team.owner:
                return Response({'message': 'You do not have permission to delete this sprint.'}, 
                                status=status.HTTP_403_FORBIDDEN)
        elif request.user != project.owner:
            return Response({'message': 'You do not have permission to delete this sprint.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        self.log_sprint_deletion(sprint)
        sprint.soft_delete()
        return Response({"message": "Sprint deleted successfully"}, status=status.HTTP_200_OK)

    

    def perform_create(self, serializer, project):
        """
        Perform the create operation for the sprint.
        """
        return serializer.save(project=project)
    
    
    logger = logging.getLogger(__name__)

    def log_sprint_creation(self, sprint):
        """
        Log the creation of a sprint.
        """
        self.logger.info(f"Sprint created - ID: {sprint.id}, Project: {sprint.project.title}")


    def log_sprint_retrieval(self, sprint):
        """
        Log the retrieval of a sprint.
        """
        self.logger.info(f"Sprint retrieved - Title: {sprint.started_at.strftime('%Y-%m-%d')}, Team: {sprint.project.workspace.team.name}")
