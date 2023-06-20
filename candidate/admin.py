from django.contrib import admin
from candidate.models import ExposedCandidate, Candidate, Designation, Skills, CandidateSkills, Tools, CandidateTools,\
    CandidateProjects, ProjectImage, Regions, CandidateRegions
from candidate.models.candidate_company import CandidateCompany

admin.site.register(CandidateCompany)
# Register your models here.
admin.site.register([ExposedCandidate, Candidate, Designation, Skills, CandidateSkills, Tools, CandidateTools,
                     CandidateProjects, ProjectImage, Regions, CandidateRegions])
