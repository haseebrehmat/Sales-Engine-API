import uuid
from django.db import models
from authentication.models import User
from settings.utils.model_fields import TimeStamped


class TeamManagement(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True)
    reporting = models.ManyToManyField('User',related_name='repoting_user', blank=True, null=True)

    def __str__(self):
        return str(self.id)
