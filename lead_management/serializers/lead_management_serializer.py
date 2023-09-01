import datetime

from django.db.models import Q
from rest_framework import serializers

from authentication.models import Team
from candidate.models import Candidate
from lead_management.models import CompanyStatus, Lead


class LeadManagementSerializer(serializers.ModelSerializer):
    leads = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CompanyStatus
        fields = ['id', 'status', 'leads']
        depth = 1

    def get_status(self, obj):
        return obj.status.name if obj.status else ''

    def get_leads(self, obj):
        role = self.context['request'].user.roles.name
        user = [str(self.context['request'].user.id)]
        current_user = self.context['request'].user

        if len(Team.objects.filter(reporting_to__in=user)) > 0:
            user.extend(
                [str(x) for x in Team.objects.filter(reporting_to__id__in=user).values_list("members__id", flat=True)])

        request = self.context['request']

        stacks = request.query_params.get('stacks', '')
        from_date = request.query_params.get('from', '')
        to_date = request.query_params.get('to', '')
        members = request.query_params.get('members', '')
        team = request.query_params.get('team', '')
        candidates = request.query_params.get('candidates', None)
        stacks_query = Q()
        from_date_query = Q()
        to_date_query = Q()
        members_query = Q()
        team_query = Q()
        candidate_query = Q()
        candidate_profile_query = Q()

        if stacks:
            stacks_query = Q(
                applied_job_status__job__tech_keywords__in=stacks.split(','))

        if from_date:
            from_date_query = Q(updated_at__gte=datetime.datetime.strptime(
                from_date, "%Y-%m-%d").date())

        if to_date:
            to_date_query = Q(
                updated_at__lt=datetime.datetime.strptime(to_date, "%Y-%m-%d").date() + datetime.timedelta(days=1))

        if team:
            team_query = Q(applied_job_status__team__id=team)

        else:
            if 'owner' not in role.lower():
                user_team = Team.objects.filter(reporting_to=current_user)
                if user_team:
                    team_query = Q(applied_job_status__team__id__in=list(
                        user_team.values_list('id', flat=True)))
                else:
                    team_query = Q(applied_job_status__applied_by=current_user)

        if members:
            members = members.split(',')
            members_query = Q(applied_job_status__applied_by__id__in=members)

        company_status_leads = Lead.objects.filter(company_status=obj)
        queryset = (company_status_leads.filter(team_query) |
                    company_status_leads.filter(converter=current_user) |
                    company_status_leads.filter(candidate__email=current_user.email))

        leads_data = queryset.filter(members_query, stacks_query, from_date_query, to_date_query, candidate_query)

        try:
            data = [{"id": str(i.id), "phase_id": str(i.phase.id) if i.phase else None,
                     "phase_name": i.phase.name if i.phase else None,
                     "applied_job": {"id": str(i.applied_job_status.id), "title": i.applied_job_status.job.job_title,
                                     "company": i.applied_job_status.job.company_name,
                                     "tech_stack": i.applied_job_status.job.tech_keywords,
                                     "applied_by": {"id": i.applied_job_status.applied_by.id,
                                                    "name": i.applied_job_status.applied_by.username},

                                     "vertical_name": i.applied_job_status.vertical.name if i.applied_job_status.vertical is not None else ""},
                     "candidate": {'id': i.candidate.id, 'name': i.candidate.name,
                                   'desigination': i.candidate.designation.title if i.candidate.designation.title else ''} if i.candidate else None, }
                    for i in leads_data if i.converter == current_user or role.lower() == "owner" or
                    role.lower() == 'candidate' or str(
                    i.applied_job_status.applied_by_id) in user]
        except Exception as e:
            print(e)
            data = []
        return data


class CustomLeadSerializer(serializers.ModelSerializer):
    phase = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    applied_job = serializers.SerializerMethodField()
    candidate = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ['id', 'phase', 'candidate', 'status', 'edited', 'applied_job', 'updated_at', 'created_at']

    def get_phase(self, instance):
        try:
            data = {'id': str(instance.phase.id) if instance.phase else None,
                    'name': instance.phase.name if instance.phase else None} if instance.phase else None
            return data
        except Exception as e:
            print("Exception in get phase => ", str(e))

    def get_status(self, instance):
        try:
            data = {'id': str(instance.company_status.id) if instance.company_status else None,
                    'name': instance.company_status.status.name if instance.company_status.status else None} if instance.company_status else None
            return data
        except Exception as e:
            print("Exception in get status => ", str(e))

    def get_applied_job(self, instance):
        try:
            applied_job = instance.applied_job_status
            data = {"id": str(applied_job.id), "title": applied_job.job.job_title,
                    "company": applied_job.job.company_name,
                    "tech_stack": applied_job.job.tech_keywords,
                    "applied_by": {"id": applied_job.applied_by.id, "name": applied_job.applied_by.username},
                    "vertical_name": applied_job.vertical.name if applied_job.vertical is not None else ""}
            return data
        except Exception as e:
            print("Exception in get applied job => ", str(e))

    def get_candidate(self, instance):
        try:
            candidate = instance.candidate
            data = {'id': candidate.id, 'name': candidate.name,
                    'desigination': candidate.designation.title if candidate.designation.title else ''} if candidate else None
            return data
        except Exception as e:
            print("Exception in get candidate => ", str(e))
