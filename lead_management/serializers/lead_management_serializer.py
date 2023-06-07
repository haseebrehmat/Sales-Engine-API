import datetime

from django.db.models import Q
from rest_framework import serializers

from authentication.models import Team
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

        if len(Team.objects.filter(reporting_to__in=user)) > 0:
            user.extend(
                [str(x) for x in Team.objects.filter(reporting_to__id__in=user).values_list("members__id", flat=True)])

        request = self.context['request']

        stacks = request.query_params.get('stacks', '')
        from_date = request.query_params.get('from', '')
        to_date = request.query_params.get('to', '')
        members = request.query_params.get('members', '')
        team = request.query_params.get('team', '')

        stacks_query = Q()
        from_date_query = Q()
        to_date_query = Q()
        members_query = Q()
        team_query = Q()

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
                current_user = self.context['request'].user
                user_team = Team.objects.filter(reporting_to=current_user)
                if user_team:
                    team_query = Q(applied_job_status__team__id__in=list(
                        user_team.values_list('id', flat=True)))
                else:
                    team_query = Q(applied_job_status__applied_by=current_user)

        if members:
            members = members.split(',')
            members_query = Q(applied_job_status__applied_by__id__in=members)

        try:
            data = [
                {
                    "id": str(i.id),
                    "phase_id": str(i.phase.id) if i.phase else None,
                    "phase_name": i.phase.name if i.phase else None,
                    "applied_job": {
                        "id": str(i.applied_job_status.id),
                        "title": i.applied_job_status.job.job_title,
                        "company": i.applied_job_status.job.company_name,
                        "tech_stack": i.applied_job_status.job.tech_keywords,
                        "applied_by": {
                            "id": i.applied_job_status.applied_by.id,
                            "name": i.applied_job_status.applied_by.username
                        },

                        "vertical_name": i.applied_job_status.vertical.name if i.applied_job_status.vertical is not None else ""
                    },
                    "candidate": {'id': i.candidate.id, 'name': i.candidate.name,
                                  'desigination': i.candidate.designation.title if i.candidate.designation.title else ''} if i.candidate else None,
                }
                for i in Lead.objects.filter(company_status=obj).filter(stacks_query, from_date_query, to_date_query,
                                                                        members_query, team_query)
                if role.lower() == "owner" or str(i.applied_job_status.applied_by_id) in user
            ]
        except Exception as e:
            print(e)
            data = []
        return data
