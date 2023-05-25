from django.db import models
from utils.model_fields import TimeStamped


class Designation(TimeStamped):
    title = models.CharField(max_length=200, unique=True)


