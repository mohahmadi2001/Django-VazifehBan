from rest_framework import serializers
from django.shortcuts import get_object_or_404

from accounts.models import Team
from .models import WorkSpace, Project, Sprint


class WorkSpaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the WorkSpace model.
    
    Serializes the WorkSpace model and specifies the fields
    to include in the response.
    """
    class Meta:
        model = WorkSpace
        fields = ('id', 'title', 'team', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    
    Serializes the Project model and specifies the fields to include in the response.
    """

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'workspace',
                  'started_at', 'ended_at', 'deadline',
                  'created_at', 'updated_at')


class SprintSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sprint model.
    
    Serializes the Sprint model and specifies the fields to include in the response.
    """

    project = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = Sprint
        fields = ('id', 'started_at', 'ended_at', 'project',
                  'tasks', 'created_at', 'updated_at')

class ProjectDetailWithSprintsSerializer(serializers.ModelSerializer):
    sprints = SprintSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'workspace', 'started_at', 'ended_at', 'deadline', 'created_at', 'updated_at', 'sprints')
        

class WorkSpaceDetailWithProjectsAndTeamSerializer(WorkSpaceSerializer):
    """
    Serializer for workspace details with projects and team information.

    Attributes:
        projects (list): A list of project objects.
        team (Team): The team object for the workspace.
    """

    projects = serializers.ListField(
        child=serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())
    )
    team = serializers.SlugRelatedField(slug_field='name', queryset=Team.objects.all())

        
        
def get_serialized_object_or_404(model_class, serializer_class, **kwargs):
    """
    Get an object with serializer or raise a 404 error if not found.
    
    Retrieves an object from the given model class based on the provided kwargs.
    Serializes the object using the specified serializer class.
    
    Parameters:
        - model_class (class): The model class to query from.
        - serializer_class (class): The serializer class to use for serialization.
        - kwargs (dict): The keyword arguments to filter the object.
        
    Returns:
        - dict: The serialized representation of the object.
        
    Raises:
        - Http404: If no object matching the kwargs is found.
    """
    instance = get_object_or_404(model_class, **kwargs)
    serializer = serializer_class(instance)
    return serializer.to_representation(instance)


def get_workspace_by_id(workspace_id: int) -> dict:
    """
    Get a workspace by ID.
    
    Retrieves a workspace with the specified ID.
    
    Parameters:
        - workspace_id (int): The ID of the workspace to retrieve.
        
    Returns:
        - dict: The serialized representation of the workspace.
        
    Raises:
        - Http404: If no workspace with the specified ID is found.
    """
    return get_serialized_object_or_404(WorkSpace, WorkSpaceSerializer, pk=workspace_id)


def get_project_by_id(project_id: int) -> dict:
    """
    Get a project by ID.
    
    Retrieves a project with the specified ID.
    
    Parameters:
        - project_id (int): The ID of the project to retrieve.
        
    Returns:
        - dict: The serialized representation of the project.
        
    Raises:
        - Http404: If no project with the specified ID is found.
    """
    return get_serialized_object_or_404(Project, ProjectSerializer, pk=project_id)


def get_sprint_by_id(sprint_id: int) -> dict:
    """
    Get a sprint by ID.
    
    Retrieves a sprint with the specified ID.
    
    Parameters:
        - sprint_id (int): The ID of the sprint to retrieve.
        
    Returns:
        - dict: The serialized representation of the sprint.
        
    Raises:
        - Http404: If no sprint with the specified ID is found.
    """
    return get_serialized_object_or_404(Sprint, SprintSerializer, pk=sprint_id)