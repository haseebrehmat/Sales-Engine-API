from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Candidate, Skills, ExposedCandidate
from candidate.serializers.candidate import CandidateSerializer
from candidate.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class SelectedCandidateListView(ListAPIView):
    serializer_class = CandidateSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

    def get_queryset(self):
        company = self.request.user.profile.company
        skills = self.request.GET.get('skills', '')
        designations = self.request.GET.get('designations', '')

        queryset = Candidate.objects.filter(company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)
        queryset |= Candidate.objects.filter(id__in=candidates)

        if len(skills) > 0:
            queryset = queryset.filter(candidateskills__skill_id__in=skills.split(','))
        if len(designations) > 0:
            queryset = queryset.filter(designation_id__in=designations.split(','))
        return queryset


