from django.urls import path

from candidate.views.candidate import CandidateDetailView, CandidateListView
from candidate.views.candidate_skill import CandidateSkillsListView, CandidateSkillsDetailView
from candidate.views.skill import SkillsDetailView, SkillsListView
from candidate.views.designation import DesignationDetailView, DesignationListView

urlpatterns = [
   path("candidate/<str:pk>/", CandidateDetailView.as_view()),
   path("candidate/", CandidateListView.as_view()),
   path("skills/<str:pk>/", SkillsDetailView.as_view()),
   path("skills/", SkillsListView.as_view()),
   path("candidate_skills/<str:pk>/", CandidateSkillsDetailView.as_view()),
   path("candidate_skills/", CandidateSkillsListView.as_view()),
   path("designation/", DesignationListView.as_view()),
   path("designation/<str:pk>/", DesignationDetailView.as_view()),
]
