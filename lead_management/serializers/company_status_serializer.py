from rest_framework import serializers

from lead_management.models import CompanyStatus, Phase


class CompanyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStatus
        fields = ['id', 'is_active', 'status']
        depth = 1


class CompanyStatusPhasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStatus
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.status:
            representation['name'] = instance.status.name
            representation['phases'] = self.get_phases(instance.id)
        return representation

    def get_phases(self, company_status_id):
        from .phase_serializer import PhaseNameSerializer
        queryset = Phase.objects.filter(company_status_id=company_status_id)
        serializer = PhaseNameSerializer(queryset, many=True)
        return serializer.data
