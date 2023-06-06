from django.db.models.functions import Lower
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from authentication.models import Team
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
        candidates = ExposedCandidate.objects.filter(company=company).values_list('candidate_id', flat=True)
        queryset |= Candidate.objects.filter(id__in=candidates)
        queryset = CandidateSkills.objects.filter(candidate__in=queryset)

        data = [
            {
                'value': x.skill.id,
                'label': x.skill.name,
            }
            for x in queryset.distinct('skill__name')
        ]
        return data

    def get_designation_options(self):
        queryset = Designation.objects.annotate(handle_lower=Lower('title')).distinct('handle_lower')
        data = [
            {
                'value': x.id,
                'label': x.title.upper(),
            }
            for x in queryset
        ]
        return data


class LeadManagementPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'num_pages': self.page.paginator.num_pages,
            'results': data,
        }
        if 'owner' in str(self.request.user.roles).lower():
            response['team'] = self.get_team()
            response['members'] = self.get_members()
        elif Team.objects.filter(reporting_to=self.request.GET.get("team")).exists():
            response['members'] = self.get_members()
        return Response(response)

    def get_team(self):
        teams = Team.objects.filter(reporting_to__profile__company=self.request.user.profile.company)
        return [{'value': str(team.id), 'label': team.name} for team in teams]

    def get_members(self):
        if "owner" in str(self.request.user.roles).lower():
            qs = Team.objects.filter(reporting_to__profile__company=self.request.user.profile.company)
        else:
            qs = Team.objects.filter(id=self.request.GET.get("team", "799af7cd-51db-4b8f-8bfb-279cbd9491ea"))
        data = []
        for i in qs:
            members = i.members.all()
            data.extend([{'value': str(x.id), 'label': x.username, "email": x.email} for x in members])
        return data

    def get_companies_options(self):
        queryset = Designation.objects.annotate(handle_lower=Lower('title')).distinct('handle_lower')
        data = [
            {
                'value': x.id,
                'label': x.title.upper(),
            }
            for x in queryset
        ]
        return data

