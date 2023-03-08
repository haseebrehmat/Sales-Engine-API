from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.forms import BaseInlineFormSet, forms

from authentication.models import User, Role, Profile, CustomPermission
from authentication.models.company import Company, CompanyAPIIntegration
from authentication.models.team_management import Team


# Register your models here.
class UserProfileInlineAdmin(admin.StackedInline):
    model = Profile
    max_num = 1
    delete = False
  

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username','is_superuser','email','company_profile', 'roles')
    list_filter = ('email','roles',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'is_superuser', 'password', 'roles', 'is_active')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    def company_profile(self, x):
        if x.profile.company:
            return x.profile.company.name
    
    company_profile.short_description = 'company'

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('email','roles')}),
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    filter_horizontal = ()

    inlines = [UserProfileInlineAdmin,]


# class CustomUserAdmin(BaseUserAdmin):
#     list_display = ('id', 'username', 'email','userprofile')
#     list_filter = ('is_admin',)
#
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#
#     add_fieldsets = BaseUserAdmin.add_fieldsets + (
#         (None, {'fields': ('email',)}),
#     )
#
#     search_fields = ('username', 'email')
#     ordering = ('username', 'email')
#
#     filter_horizontal = ()

# inlines = [TeamManagementInline]

# class TeamManagementAdmin(admin.ModelAdmin):
#
#     # A template for a very customized change view:
#     # change_form_template = 'admin/my_change_form.html'
#
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#
#         if db_field.name == "reporting" and request.method == 'GET' and request.build_absolute_uri().split('/')[
#             -2] == 'add':
#             selected_users = TeamManagement.objects.filter(reporting__groups__name='BD').values_list('reporting__id')
#             kwargs["queryset"] = User.objects.exclude(id__in=selected_users).exclude(groups__name='TL')
#         elif db_field.name == "reporting" and request.method == 'GET' and request.build_absolute_uri().split('/')[
#             -2] == 'change':
#             selected_users = TeamManagement.objects.filter(reporting__groups__name='BD').values_list('reporting__id')
#             kwargs["queryset"] = User.objects.filter(id__in=selected_users).exclude(groups__name='TL')
#
#         return super().formfield_for_manytomany(db_field, request, **kwargs)

# def formfield_for_foreignkey(self, db_field, request, **kwargs):
#     print(db_field.name)
#     if db_field.name == "user":
#         kwargs["queryset"] = User.objects.filter(groups__name='TL')
#     return super().formfield_for_foreignkey(db_field, request, **kwargs)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name','company', 'description',)
    list_filter = ('company',)




admin.site.register(User, UserAdmin)
admin.site.register([CustomPermission, Company,Profile, CompanyAPIIntegration])
admin.site.register(Team)
admin.site.unregister(Group)
admin.site.register(Role,RoleAdmin)
