from django.contrib import admin
from candidate.models import ExposedCandidate, Candidate, Designation

# Register your models here.
admin.site.register([ExposedCandidate, Candidate, Designation])
