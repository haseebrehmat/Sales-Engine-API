from rest_framework import status, filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Candidate, Skills, ExposedCandidate, CandidateRegions, SelectedCandidate
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
        regions = self.request.GET.get('regions', '')
        queryset = Candidate.objects.filter(company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)
        if regions:
            regions = regions.split(',')
            candidates_regions = CandidateRegions.objects.filter(region__id__in=regions)
            valid_candidates = list(candidates_regions.values_list('candidate__id', flat=True))
            queryset = queryset.filter(id__in=valid_candidates)
            candidates = candidates.filter(candidate__id__in=valid_candidates)
        queryset |= Candidate.objects.filter(id__in=candidates)
        selected_candidates = SelectedCandidate.objects.filter(company=company, status=True)
        queryset = queryset.filter(id__in=selected_candidates.values_list('candidate_id', flat=True))
        if len(skills) > 0:
            queryset = queryset.filter(candidateskills__skill_id__in=skills.split(','))
        if len(designations) > 0:
            queryset = queryset.filter(designation_id__in=designations.split(','))
        return queryset.distinct("id")


