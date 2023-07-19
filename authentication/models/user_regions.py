from django.db import models

from settings.utils.model_fields import TimeStamped
from authentication.models import User
from candidate.models import Regions

class UserRegions(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, blank=True, null=True)