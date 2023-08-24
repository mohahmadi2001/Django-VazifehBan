from django.urls import path
from .views import (
                    UserRegistrationView,
                    UserUpdateView,
                    CustomSetPasswordView,
                    UserDeleteView
                )


app_name = 'accounts'
urlpatterns = [
    path('user/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/update/', UserUpdateView.as_view(), name='user-profile-update'),
    path('user/password_change/', CustomSetPasswordView.as_view(), name='password-change'),
    path('user/delete-user/', UserDeleteView.as_view(), name='delete-user'),
]