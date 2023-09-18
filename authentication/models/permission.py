import uuid

from django.db import models

from settings.utils.model_fields import TimeStamped


class CustomPermission(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        max_length=36,
        editable=False)
    module = models.CharField(blank=False, null=False, max_length=200, default="nothing")
    codename = models.CharField(blank=False, null=False, max_length=200, default="nothing")
    name = models.CharField(blank=False, null=False, max_length=200, default="nothing")
    level = models.CharField(blank=False, null=False, max_length=10, default=1)
    child = models.JSONField(blank=True, null=True)
    parent = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ("module",)
        unique_together = ('module', 'codename', 'name')

    def __str__(self):
        return f"{self.module} - {self.name} - {self.codename}- {self.level}"
