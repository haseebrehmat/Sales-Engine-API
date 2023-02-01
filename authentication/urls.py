from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views.group import GroupView, GroupDetailView
from authentication.views.users import LoginView
from authentication.views.permission import PermissionView, PermissionDetailView
from authentication.views.users import UserPermission

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('group/', GroupView.as_view()),
    path('group/<str:pk>/', GroupDetailView.as_view()),
    path('permission/', PermissionView.as_view()),
    path('permission/<str:pk>/', PermissionDetailView.as_view()),
    path('user_permission/<str:pk>/', UserPermission.as_view()),
]
