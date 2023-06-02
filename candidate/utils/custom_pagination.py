from django.db.models.functions import Lower
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from candidate.models import CandidateSkills, Skills, Designation, Candidate, ExposedCandidate


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'num_pages': self.page.paginator.num_pages,
            'results': data,
            'skills': self.get_skill_options(),
            'designations': self.get_designation_options(),
        })
        return response

    def get_skill_options(self):
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list("candidate_id", flat=True)
        queryset |= Candidate.objects.filter(id__in=candidates)
        queryset = CandidateSkills.objects.filter(candidate__in=queryset)

        data = [
            {
                'value': x.skill.id,
                'label': x.skill.name,
            }
            for x in queryset.distinct("skill__name")
        ]
        return data

    def get_designation_options(self):
        queryset = Designation.objects.annotate(handle_lower=Lower("title")).distinct("handle_lower")
        data = [
            {
                'value': x.id,
                'label': x.title.upper(),
            }
            for x in queryset
        ]
        return data
