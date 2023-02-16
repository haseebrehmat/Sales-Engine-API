from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.forms import BaseInlineFormSet, forms

from authentication.models import User
from authentication.models.team_management import TeamManagement

# Register your models here.

class TeamManagementInlineFormSet(BaseInlineFormSet):

    def get_queryset(self):
        qs = super(TeamManagementInlineFormSet, self).get_queryset()
        return qs.filter()
class TeamManagementInline(admin.StackedInline):
    model = TeamManagement
    max_num = 1
    formset = TeamManagementInlineFormSet
    can_delete = False
    readonly_fields = ["reporting",]


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "reporting":
            selected_users = TeamManagement.objects.get(user=request.user.id).reporting.values_list('id')
            selected_users_list = [i[0] for i in selected_users]
            kwargs["queryset"] = User.objects.filter(pk__in=selected_users_list)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id','username', 'email')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),

        ('Permissions', {'fields': ('is_admin',)}),
        ('Groups',{'fields':('groups',)})
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email')

    filter_horizontal = ()
    inlines = [TeamManagementInline]



class TeamManagementAdmin(admin.ModelAdmin):

    # A template for a very customized change view:
    # change_form_template = 'admin/my_change_form.html'

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == "reporting" and request.method == 'GET' and request.build_absolute_uri().split('/')[
            -2] == 'add':
            selected_users = TeamManagement.objects.filter(reporting__groups__name='BD').values_list('reporting__id')
            kwargs["queryset"] = User.objects.exclude(id__in=selected_users).exclude(groups__name='TL')

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(groups__name='TL')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(User, CustomUserAdmin)
admin.site.register(TeamManagement, TeamManagementAdmin)
admin.site.register([Permission])