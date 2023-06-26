from django.db import models
from utils.model_fields.timestamped import TimeStamped
from settings.utils.model_fields import LowercaseEmailField

class Accounts(TimeStamped):
    email = LowercaseEmailField(unique=True)
    password = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return f"{self.email}"