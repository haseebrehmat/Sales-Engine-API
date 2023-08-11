import uuid

from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomPermission
from settings.utils.model_fields import TimeStamped


class Role(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(blank=True, null=True, max_length=100)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(CustomPermission)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")
        default_permissions = ()
        db_table = "role"

    def __str__(self):
        return f'{self.name}'


class MultipleRoles(TimeStamped):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'user')
