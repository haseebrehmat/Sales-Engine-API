import uuid

from django.db import models

from settings.utils.model_fields import TimeStamped


class CustomPermission(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        max_length=36,
        editable=False)
    module = models.CharField(max_length=200)
    codename = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    level = models.CharField(blank=True, null=True, max_length=10)

    class Meta:
        ordering = ("module",)
        unique_together = ('module', 'codename', 'name')

    def __str__(self):
        return f"{self.module} - {self.name} - {self.codename}- {self.level}"
