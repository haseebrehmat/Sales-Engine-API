from django.db.models.functions import Lower
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from authentication.models import Team, Profile
from candidate.models import CandidateSkills, Designation, Candidate, ExposedCandidate, SelectedCandidate, Regions
from job_portal.models import JobDetail, AppliedJobStatus


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = Response(
            {'count': self.page.paginator.count, 'next': self.get_next_link(), 'previous': self.get_previous_link(),
             'num_pages': self.page.paginator.num_pages, 'results': data, 'skills': self.get_skill_options(),
             'designations': self.get_designation_options(), 'regions': self.get_regions(), })
        return response

    def get_skill_options(self):
        company = self.request.user.profile.company
        queryset = Candidate.objects.filter(company=company)
        candidates = ExposedCandidate.objects.filter(company=company).values_list('candidate_id', flat=True)
        queryset |= Candidate.objects.filter(id__in=candidates)
        queryset = CandidateSkills.objects.filter(candidate__in=queryset)

        data = [{'value': x.skill.id, 'label': x.skill.name, } for x in queryset.distinct('skill__name')]
        return data

    def get_designation_options(self):
        queryset = Designation.objects.annotate(handle_lower=Lower('title')).distinct('handle_lower')
        data = [{'value': x.id, 'label': x.title.upper(), } for x in queryset]
        return data

    def get_regions(self):
        data = [{'label': obj.region, 'value': obj.id } for obj in Regions.objects.all()]
        return data

class LeadManagementDataPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = {'count': self.page.paginator.count, 'next': self.get_next_link(),
                    'previous': self.get_previous_link(), 'num_pages': self.page.paginator.num_pages, 'results': data}
        return Response(response)




class LeadManagementPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'limit'
    max_page_size = 250

    def get_paginated_response(self, data):
        response = {'count': self.page.paginator.count, 'next': self.get_next_link(),
                    'previous': self.get_previous_link(), 'num_pages': self.page.paginator.num_pages, 'results': data}

        if 'owner' in str(self.request.user.roles).lower():
            response['team'] = self.get_team()
            response['members'] = self.get_members()
        else:
             team = Team.objects.filter(reporting_to=self.request.user).first()
             if team:
                response['members'] = self.get_members()
        response['tech_stack'] = self.get_tech_stack()
        response['candidates'] = self.get_candidates()
        return Response(response)

    def get_team(self):
        if 'owner' in str(self.request.user.roles).lower():
            teams = Team.objects.filter(reporting_to__profile__company=self.request.user.profile.company)
        else:
            teams = Team.objects.filter(reporting_to=self.request.user)
        return [{'value': str(team.id), 'label': team.name} for team in teams]

    def get_members(self):
        if "owner" in str(self.request.user.roles).lower():
            qs = Team.objects.filter(reporting_to__profile__company=self.request.user.profile.company)
        else:
            qs = Team.objects.filter(reporting_to=self.request.user)
        data = []
        users_id = []
        for i in qs:
            members = i.members.all()
            for x in members:
                if x.id not in users_id:
                    users_id.append(x.id)
                    data.extend([{'value': str(x.id), 'label': x.username.lower(), 'team': [i.id]}])
                else:
                    index = next((index for index, item in enumerate(data) if item.get('value') == str(x.id)), None)
                    data[index]['team'].append(i.id)
        return data

    def get_companies_options(self):
        queryset = Designation.objects.annotate(handle_lower=Lower('title')).distinct('handle_lower')
        data = [{'value': x.id, 'label': x.title.upper(), } for x in queryset]
        return data

    def get_applied_job_ids(self):
        company_user_ids = list(
            Profile.objects.filter(company=self.request.user.profile.company).values_list('user__id', flat=True))
        return list(AppliedJobStatus.objects.filter(applied_by__in=company_user_ids).values_list('job__id', flat=True))

    def get_tech_stack(self):
        tech_stack = list(dict.fromkeys(stack.lower() for stack in list(
            JobDetail.objects.filter(id__in=self.get_applied_job_ids()).values_list('tech_keywords', flat=True))))
        return self.format_list(tech_stack)

    def get_companies(self):
        company_names = list(dict.fromkeys(company.lower() for company in list(
            JobDetail.objects.filter(id__in=self.get_applied_job_ids()).values_list('company_name', flat=True))))
        return self.format_list(company_names)

    def get_candidates(self):
        selected_candidates = SelectedCandidate.objects.filter(company=self.request.user.profile.company, status=True)
        candidates_data = [{'label': obj.candidate.name, 'value': obj.candidate.id } for obj in selected_candidates]
        return candidates_data

    def format_list(self, list_items):
        return [{'label': item, 'value': item} for item in list_items]
