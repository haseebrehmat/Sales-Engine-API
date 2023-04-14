from django.db import models

from pseudos.models import Verticals
from utils.model_fields.timestamped import TimeStamped


class CoverLetter(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    template = models.TextField()
