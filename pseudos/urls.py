from django.urls import path
from pseudos.views.certificates import CertificateView, CertificateDetailView
from pseudos.views.education import EducationView, EducationDetailView
from pseudos.views.experience import ExperienceView, ExperienceDetailView
from pseudos.views.languages import LanguageView, LanguageDetailView
from pseudos.views.links import LinkView, LinkDetailView
from pseudos.views.other_sections import OtherSectionView, OtherSectionDetailView
from pseudos.views.pseudos import PseudosView, PseudoDetailView
from pseudos.views.resume import ResumeView
# from pseudos.views.resume_section import ResumeSectionDetailView, ResumeSectionView
from pseudos.views.skills import SkillView, SkillDetailView
from pseudos.views.verticals import VerticalView, VerticalDetailView

urlpatterns = [
    path('pseudo/', PseudosView.as_view()),
    path('pseudo/<str:pk>/', PseudoDetailView.as_view()),
    path('vertical/', VerticalView.as_view()),
    path('vertical/<str:pk>/', VerticalDetailView.as_view()),
    path('resume/<str:pk>/', ResumeView.as_view()),
    path('skill/', SkillView.as_view()),
    path('skill/<str:pk>/', SkillDetailView.as_view()),
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
    path('other_section/', OtherSectionView.as_view()),
    path('other_section/<str:pk>/', OtherSectionDetailView.as_view()),

]
