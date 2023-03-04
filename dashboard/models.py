from django.db import models

# Create your models here.


class Dashboard(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions

        permissions = (
            ("view_dashboard", "view dashboard"),
        )
