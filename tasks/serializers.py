from rest_framework import serializers
from .models import Task, Label, TaskLabel, Comment, Attachment, WorkTime


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabel
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class WorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTime
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    labels = TaskLabelSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    work_times = WorkTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        labels_data = validated_data.pop('labels', [])
        comments_data = validated_data.pop('comments', [])
        attachments_data = validated_data.pop('attachments', [])
        work_times_data = validated_data.pop('work_times', [])

        task = Task.objects.create(**validated_data)

        for label_data in labels_data:
            TaskLabel.objects.create(task=task, **label_data)

        for comment_data in comments_data:
            Comment.objects.create(task=task, **comment_data)

        for attachment_data in attachments_data:
            Attachment.objects.create(task=task, **attachment_data)

        for work_time_data in work_times_data:
            WorkTime.objects.create(task=task, **work_time_data)

        return task
