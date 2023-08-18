from django.urls import path

from candidate.views.candidate import CandidateDetailView, CandidateListView, CandidateProfileDetailView
from candidate.views.candidate_projects import CandidateProjectDetailView
from candidate.views.candidate_company import CandidateCompanyDetailView, CandidateCompanyListView
from candidate.views.candidate_skill import CandidateSkillsListView, CandidateSkillsDetailView
from candidate.views.regions import RegionsListView, AllRegions
from candidate.views.skill import SkillsDetailView, SkillsListView
from candidate.views.designation import DesignationDetailView, DesignationListView
from candidate.views.exposed_candidates import CandidateExposedDetailView, ExposedCandidateListAPIView, PoolCandidateDetailView, PoolCandidateListAPIView
from candidate.views.selected_candidate import SelectedCandidateListView
from candidate.views.candidate_teams import CandidateTeamsListView, CandidateTeamsDetailView
from candidate.views.exposed_team import ExposedTeamListAPIView

urlpatterns = [
   path("candidate/<str:pk>/", CandidateDetailView.as_view()),
   path("candidate/", CandidateListView.as_view()),
   path("candidate_profile/", CandidateProfileDetailView.as_view()),
   path("skills/<str:pk>/", SkillsDetailView.as_view()),
   path("skills/", SkillsListView.as_view()),
   path("candidate_skills/<str:pk>/", CandidateSkillsDetailView.as_view()),
   path("candidate_projects/<str:pk>/", CandidateProjectDetailView.as_view()),
   path("candidate_skills/", CandidateSkillsListView.as_view()),
   path("designation/", DesignationListView.as_view()),
   path("designation/<str:pk>/", DesignationDetailView.as_view()),
   path("candidate_exposed/", ExposedCandidateListAPIView.as_view()),
   path("candidate_exposed/<str:pk>/", CandidateExposedDetailView.as_view()),
   path("team_exposed/", ExposedTeamListAPIView.as_view()),
   path("team_exposed/<str:pk>/", ExposedTeamListAPIView.as_view()),
   path("pool_candidate/", PoolCandidateListAPIView.as_view()),
   path("pool_candidate/<str:pk>/", PoolCandidateDetailView.as_view()),
   path("candidate_company/", CandidateCompanyListView.as_view()),
   path("candidate_teams/", CandidateTeamsListView.as_view()),
   path("candidate_teams/<str:pk>/", CandidateTeamsDetailView.as_view()),
   path("candidate_company/<str:pk>/", CandidateCompanyDetailView.as_view()),
   path("selected_candidate/", SelectedCandidateListView.as_view()),
   path("regions/", RegionsListView.as_view()),
   path("all_regions/", AllRegions.as_view()),
]
