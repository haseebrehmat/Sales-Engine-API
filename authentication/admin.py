from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from authentication.models import User
from authentication.models.team_management import TeamManagement

# Register your models here.
admin.site.register([User, Permission,TeamManagement])