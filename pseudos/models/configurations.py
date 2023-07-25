from django.db import models

from utils.model_fields.timestamped import TimeStamped


class VerticalConfigurations(TimeStamped):
    user = models.OneToOneField(
        'authentication.User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="vertical_config_user"
    )
    team = models.ForeignKey(
        'authentication.Team',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="vertical_config_team"
    )
    vertical = models.ForeignKey(
        "Verticals",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="vertical_config"
    )
    template_key = models.CharField(max_length=250, blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
