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
            user.extend([str(x) for x in Team.objects.filter(reporting_to__id__in=user).values_list("members")])

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
                        "vertical_name": i.applied_job_status.vertical.name if i.applied_job_status.vertical is not None else ""
                    }
                }
                for i in Lead.objects.filter(company_status=obj)
                if role.lower() == "owner" or str(i.applied_job_status.applied_by_id) in user
            ]
        except Exception as e:
            print(e)
            data = []
        return data
