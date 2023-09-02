from rest_framework import serializers
from .models import Task, Label, TaskLabel, Comment, Attachment, WorkTime


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'created_at', 'description', 'sprint', 'user', 'status']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabel
        fields = ['label', 'task']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created_at', 'user', 'task']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['content', 'task']


class WorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTime
        fields = ['start_date', 'end_date', 'task']
