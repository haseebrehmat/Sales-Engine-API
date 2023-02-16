import uuid
from django.db import models
from authentication.models import User
from settings.utils.model_fields import TimeStamped


class TeamsMemmbers(models.QuerySet):
    def get_memmbers(self):
        return self.reporting.values_list('id', flat=True)

        # return self.filter(applied_by__groups__name='TL')


class TeamManagementManager(models.Manager):
    def get_queryset(self):
        return TeamsMemmbers(self.model, using=self._db)


class TeamManagement(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    reporting = models.ManyToManyField('User',related_name='repoting_user')

    objects = TeamManagementManager()

    def __str__(self):
        if self.user.groups.values_list('name').count():
            return f"{self.user.username}__{self.user.groups.values_list('name')[0][0]}"
