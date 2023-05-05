from django.db import models

from authentication.models.company import Company
from pseudos.models.verticals import Verticals
from utils.model_fields.timestamped import TimeStamped


class Skills(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    generic_skill = models.ForeignKey('GenericSkills', on_delete=models.CASCADE, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "skills"
        unique_together = ("vertical", "generic_skill")
        default_permissions = ()


class GenericSkills(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "generic_skills"
        unique_together = ("name", "type", "company")
        default_permissions = ()


class Experience(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.CharField(max_length=250, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Education(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    institute = models.CharField(max_length=250, blank=True, null=True)
    degree = models.CharField(max_length=250, blank=True, null=True)
    grade = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Links(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=500)
    platform = models.CharField(max_length=250)


class Language(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    level = models.IntegerField(blank=True, null=True)


class Certificate(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    link = models.TextField(blank=True, null=True)


class OtherSection(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    value = models.JSONField(blank=True, null=True)


class Projects(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    repo = models.CharField(max_length=500, blank=True, null=True)


class SectionStatus(TimeStamped):
    vertical = models.ForeignKey(Verticals, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)

