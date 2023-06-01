from rest_framework import status
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

    def get_queryset(self):
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(
            company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)

        queryset |= Candidate.objects.filter(id__in=candidates)

        return queryset


