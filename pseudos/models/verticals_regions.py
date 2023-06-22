from django.db import models

from candidate.models import Regions
from pseudos.models import Verticals
from settings.utils.model_fields import TimeStamped


class VerticalsRegions(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True)
