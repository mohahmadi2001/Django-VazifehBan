# from django.urls import include, path
# from .views import ProjectCreateView, ProjectDeleteView, ProjectDetailView, ProjectEditView, SprintCreateView, SprintDeleteView, SprintDetailView, SprintEditView, WorkSpaceCreateView,  WorkSpaceDeleteView, WorkSpaceDetailView, WorkSpaceEditView, WorkSpaceViewSet
# from rest_framework import routers


# urlpatterns = [
#     # Workspace URLs
    
   
#     path('workspaces/create/', WorkSpaceCreateView.as_view(), name='create-workspace'),
#     path('workspaces/<int:pk>/', WorkSpaceDetailView.as_view(), name='workspace-detail'),
#     path('workspaces/<int:pk>/edit/', WorkSpaceEditView.as_view(), name='workspace-edit'),
#     path('workspaces/<int:pk>/delete/', WorkSpaceDeleteView.as_view(), name='workspace-delete'),

#     # Project URLs
#     path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
#     path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
#     path('projects/<int:pk>/edit/', ProjectEditView.as_view(), name='project-edit'),
#     path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

#     # Sprint URLs
#     path('sprints/create/', SprintCreateView.as_view(), name='sprint-create'),
#     path('sprints/<int:pk>/edit/', SprintEditView.as_view(), name='sprint-edit'),
#     path('sprints/<int:pk>/', SprintDetailView.as_view(), name='sprint-detail'),
#     path('sprints/<int:pk>/delete/', SprintDeleteView.as_view(), name='sprint-delete'),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, SprintViewSet, WorkSpaceViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'workspaces', WorkSpaceViewSet, basename='workspace')
router.register(r'sprints', SprintViewSet, basename='sprint')

router.lookup_field = 'pk'

urlpatterns = [
    path('', include(router.urls)),
    
    
   
]