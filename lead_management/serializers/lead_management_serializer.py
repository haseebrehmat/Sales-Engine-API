from rest_framework import serializers

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
        print()
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
                        "tech_stack": i.applied_job_status.job.tech_keywords
                    }
                }
                for i in Lead.objects.filter(company_status=obj)
            ]
        except:
            data = []
        return data
