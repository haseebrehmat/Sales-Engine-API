import uuid
from django.db import models

from authentication.models import Role
from settings.utils.model_fields import TimeStamped
from pseudos.models.verticals import Verticals


class TeamsMemmbers(models.QuerySet):
    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)

    def get_memmbers(self):
        return self.reporting_to.values_list('id', flat=True)


class TeamManagementManager(models.Manager):
    def get_queryset(self):
        return TeamsMemmbers(self.model, using=self._db)


class Team(TimeStamped):
    reporting_to = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
    members = models.ManyToManyField('User', related_name='reporting_user')
    verticals = models.ManyToManyField(Verticals, related_name='verticals', blank=True)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, blank=True, null=True)

    objects = TeamManagementManager()

    def __str__(self):
        return f"{self.reporting_to.username}"

    class Meta:
        db_table = "team"
        default_permissions = ()


class TeamRoleVerticalAssignment(TimeStamped):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='team_verticals', blank=True)
    member = models.ForeignKey('User', on_delete=models.CASCADE, related_name='team_members', blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team', blank=True)
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, related_name='team_role_vertical', blank=True)

    class Meta:
        unique_together = ('role', 'member', 'team', 'vertical')
