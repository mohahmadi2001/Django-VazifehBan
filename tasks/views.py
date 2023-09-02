from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Task, Comment, Attachment, WorkTime, Label
from .serializers import TaskSerializer, CommentSerializer, AttachmentSerializer, WorkTimeSerializer


# Create Task
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # Add owner permission logic here
        serializer.save()


# Retrieve Task Information
class TaskRetrieveView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Update Task
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Delete Task
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Assign Task to User
class AssignTaskView(views.APIView):
    def post(self, request, task_id):
        # Implement assignment logic here
        return Response(status=status.HTTP_200_OK)


# Attach Label to Task
class AttachLabelView(views.APIView):
    def post(self, request, task_id):
        # Implement label attachment logic here
        return Response(status=status.HTTP_200_OK)


# Create Comment for Task
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Delete Comment
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Add Attachment to Task
class AttachmentCreateView(generics.CreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# Delete Attachment
class AttachmentDeleteView(generics.DestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


# Add WorkTime for Task and User
class WorkTimeCreateView(generics.CreateAPIView):
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer


# Complete WorkTime
class WorkTimeCompleteView(views.APIView):
    def post(self, request, worktime_id):
        # Implement worktime completion logic here
        return Response(status=status.HTTP_200_OK)
