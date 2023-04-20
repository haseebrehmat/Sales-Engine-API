from django.db import models

from authentication.models.company import Company
from pseudos.models.pseudos import Pseudos
from utils.model_fields.timestamped import TimeStamped

# choices = [
#     ('basic', 'Basic'),
#     ('summary', 'Summary'),
#     ('experience', 'Experience'),
#     ('education', 'Education'),
#     ('skill', 'Skill'),
#     ('certificate', 'Certificate'),
#     ('hobby', 'Hobby'),
#     ('link', 'Link'),
#     ('other', 'Other')
# ]


class Verticals(TimeStamped):
    pseudo = models.ForeignKey(Pseudos, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250)
    identity = models.CharField(max_length=250, blank=True, null=True)
    hidden = models.BooleanField(default=False)
    email = models.EmailField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    show_summary = models.BooleanField(default=True)
    hobbies = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

