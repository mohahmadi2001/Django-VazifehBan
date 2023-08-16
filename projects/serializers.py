from rest_framework import serializers
from .models import WorkSpace, Project, Sprint


class WorkSpaceSerializer(serializers.ModelSerializer):
    """Serializer for the WorkSpace model."""

    class Meta:
        model = WorkSpace
        fields = ('id', 'title', 'team', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the Project model."""

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'workspace',
                  'started_at', 'ended_at', 'deadline',
                  'created_at', 'updated_at')


class SprintSerializer(serializers.ModelSerializer):
    """Serializer for the Sprint model."""

    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Sprint
        fields = ('id', 'started_at', 'ended_at', 'project',
                  'tasks', 'created_at', 'updated_at')