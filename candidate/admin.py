from django.contrib import admin
from candidate.models import ExposedCandidate, Candidate
# Register your models here.
admin.site.register(ExposedCandidate)
admin.site.register(Candidate)