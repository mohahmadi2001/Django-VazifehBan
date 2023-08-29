from django.urls import path
from .views import (
    UserRegistrationView,
    UserUpdateView,
    CustomSetPasswordView,
    UserDeleteView,
    UserDetailView, TeamView, UserTeamView
)

app_name = 'accounts'
urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/update/', UserUpdateView.as_view(), name='user-profile-update'),
    path('user/password_change/', CustomSetPasswordView.as_view(), name='password-change'),
    path('user/delete-user/', UserDeleteView.as_view(), name='delete-user'),
    path('user/detail/', UserDetailView.as_view(), name='user-detail'),
    path('team/', TeamView.as_view(), name='team-list-create'),
    path('team/<int:pk>/', TeamView.as_view(), name='team-detail-update'),
    path('userteam/', UserTeamView.as_view(), name='userteam-list-create'),
    path('userteam/<int:pk>/', UserTeamView.as_view(), name='userteam-detail'),

]
