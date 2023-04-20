import uuid
from django.db import models
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
