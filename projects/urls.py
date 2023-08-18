from django.urls import path
from .views import ProjectCreateView, SprintCreateView, WorkSpaceCreateView, WorkSpaceDeleteView, WorkSpaceDetailView, WorkSpaceEditView

urlpatterns = [
   
    path('create/workspace/', WorkSpaceCreateView.as_view(), name='create-workspace'),
    path('teams/<int:team_pk>/workspaces/<int:workspace_pk>/edit/', WorkSpaceEditView.as_view(), name='workspace-edit'),
    path('workspaces/<int:pk>/', WorkSpaceDetailView.as_view(), name='workspace-detail'),
    path('workspaces/<int:pk>/delete/', WorkSpaceDeleteView.as_view(), name='workspace-delete'),

    path('workspaces/<int:workspace_pk>/projects/create/', ProjectCreateView.as_view(), name='project-create'),

    path('projects/<int:project_pk>/sprints/create/', SprintCreateView.as_view(), name='sprint-create'),
]