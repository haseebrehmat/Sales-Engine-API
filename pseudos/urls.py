from django.urls import path
from pseudos.views.certificates import CertificateView, CertificateDetailView
from pseudos.views.configurations import ConfigurationView
from pseudos.views.cover_letter import CoverLetterView, CoverLetterDetailView
from pseudos.views.education import EducationView, EducationDetailView
from pseudos.views.experience import ExperienceView, ExperienceDetailView
from pseudos.views.generate_cover_letter import GenerateCoverLetter
from pseudos.views.languages import LanguageView, LanguageDetailView
from pseudos.views.links import LinkView, LinkDetailView
from pseudos.views.other_sections import OtherSectionView, OtherSectionDetailView
from pseudos.views.projects import ProjectView, ProjectDetailView
from pseudos.views.pseudos import PseudosView, PseudoDetailView
from pseudos.views.resume import ResumeView
from pseudos.views.skills import SkillView, SkillDetailView, GenericSkillView, GenericSkillDetailView
from pseudos.views.sectionstatus import SectionStatusView
from pseudos.views.verticals import VerticalView, VerticalDetailView
from pseudos.views.team_verticals_assignment import TeamVerticalsAssignView, UserVerticalsAssignView, UserVerticals, \
    JobVerticals

urlpatterns = [
    path('pseudo/', PseudosView.as_view()),
    path('pseudo/<str:pk>/', PseudoDetailView.as_view()),
    path('vertical/', VerticalView.as_view()),
    path('vertical/<str:pk>/', VerticalDetailView.as_view()),
    path('resume/<str:pk>/', ResumeView.as_view()),
    path('skill/', SkillView.as_view()),
    path('skill/<str:pk>/', SkillDetailView.as_view()),
    path('generic_skill/', GenericSkillView.as_view()),
    path('generic_skill/<str:pk>/', GenericSkillDetailView.as_view()),
    path('experience/', ExperienceView.as_view()),
    path('experience/<str:pk>/', ExperienceDetailView.as_view()),
    path('education/', EducationView.as_view()),
    path('education/<str:pk>/', EducationDetailView.as_view()),
    path('links/', LinkView.as_view()),
    path('links/<str:pk>/', LinkDetailView.as_view()),
    path('language/', LanguageView.as_view()),
    path('language/<str:pk>/', LanguageDetailView.as_view()),
    path('certificate/', CertificateView.as_view()),
    path('certificate/<str:pk>/', CertificateDetailView.as_view()),
    path('cover_letter/', CoverLetterView.as_view()),
    path('cover_letter/<str:pk>/', CoverLetterDetailView.as_view()),
    path('generate/cover_letter/', GenerateCoverLetter.as_view()),
    path('other_section/', OtherSectionView.as_view()),
    path('other_section/<str:pk>/', OtherSectionDetailView.as_view()),
    path('project/', ProjectView.as_view()),
    path('project/<str:pk>/', ProjectDetailView.as_view()),
    path('team_vertical_assignment/', TeamVerticalsAssignView.as_view()),
    path('user_vertical_assignment/', UserVerticalsAssignView.as_view()),
    path('user_vertical/', UserVerticals.as_view()),
    path('job_vertical/', JobVerticals.as_view()),
    path('section_status/<str:pk>/', SectionStatusView.as_view()),
    # path('configuration/', ConfigurationView.as_view()),

]
