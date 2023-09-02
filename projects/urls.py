

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