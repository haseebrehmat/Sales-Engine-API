from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views.create_permissions import CreatePermissions
from authentication.views.authenticate import UserLogin
from authentication.views.company import CompanyView, CompanyDetailView
from authentication.views.integrations import IntegrationView, IntegrationDetailView
from authentication.views.multiple_role import MultipleRoleManagement
from authentication.views.password.change import PasswordManagement
from authentication.views.password.reset import PasswordReset
from authentication.views.profile import ProfileView
from authentication.views.profile_image import ProfileViewImage
from authentication.views.reset_password import render_reset_page
from authentication.views.role import RoleView, RoleDetailView, RoleUserView, AllRoleView
from authentication.views.team_management import TeamView, TeamDetailView
from authentication.views.user_regions import UserRegionsList
from authentication.views.users import LoginView, UserView, UserDetailView
from authentication.views.permission import PermissionView, PermissionDetailView, get_all_permissions, \
    PermissionAssignmentView
from authentication.views.users import UserPermission

urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('authenticate/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('permission/', PermissionView.as_view()),
    path('permission_assignment/', PermissionAssignmentView.as_view()),
    path('all_permissions/', get_all_permissions),
    path('permission/<str:pk>/', PermissionDetailView.as_view()),
    path('user_permission/<str:pk>/', UserPermission.as_view()),
    path('password/change/', PasswordManagement.as_view()),
    path('password/reset/', PasswordReset.as_view()),
    path('reset/<str:email>/<str:code>/', render_reset_page),
    path('company/', CompanyView.as_view()),
    path('company/<str:pk>/', CompanyDetailView.as_view()),
    path('integration/', IntegrationView.as_view()),
    path('integration/<str:pk>/', IntegrationDetailView.as_view()),
    path('team/', TeamView.as_view()),
    path('team/<str:pk>/', TeamDetailView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<str:pk>/', UserDetailView.as_view()),
    path('user_profile/', ProfileView.as_view()),
    path('user_profile_image/', ProfileViewImage.as_view()),
    path('role/', RoleView.as_view()),
    path('role/<str:pk>/', RoleDetailView.as_view()),
    path('role_users/<str:pk>/', RoleUserView.as_view()),
    path('create_permissions/', CreatePermissions.as_view()),
    path('user_regions/', UserRegionsList.as_view()),
    path('roles/', MultipleRoleManagement.as_view()),
    path('all_roles/', AllRoleView.as_view()),
    path('roles/', MultipleRoleManagement.as_view()),
]
