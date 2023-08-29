from django.urls import path
from . import views

urlpatterns = [
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:task_id>/assign/', views.AssignTaskView.as_view(), name='task-assign'),
    path('tasks/<int:task_id>/attach-label/', views.AttachLabelView.as_view(), name='attach-label'),
    path('comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('attachments/create/', views.AttachmentCreateView.as_view(), name='attachment-create'),
    path('attachments/<int:pk>/delete/', views.AttachmentDeleteView.as_view(), name='attachment-delete'),
    path('worktimes/create/', views.WorkTimeCreateView.as_view(), name='worktime-create'),
    path('worktimes/<int:worktime_id>/complete/', views.WorkTimeCompleteView.as_view(), name='worktime-complete'),
]
