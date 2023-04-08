from django.db import models

from authentication.models.company import Company
from pseudos.models.verticals import Verticals
from utils.model_fields.timestamped import TimeStamped


class Skills(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)


class Experience(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.CharField(max_length=250, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Education(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    institute = models.CharField(max_length=250, blank=True, null=True)
    degree = models.CharField(max_length=250, blank=True, null=True)
    grade = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)


class Links(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=500)
    platform = models.CharField(max_length=250)


class Language(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    level = models.IntegerField(blank=True, null=True)


class Certificate(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    link = models.TextField(blank=True, null=True)


class OtherSection(TimeStamped):
    verticals = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    value = models.JSONField(blank=True, null=True)
