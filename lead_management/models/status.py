from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=30, null=True, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        default_permissions = ()
        db_table = "status"

    def __str__(self):
        return self.name
