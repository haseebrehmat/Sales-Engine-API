from rest_framework import serializers

from candidate.models.candidate_company import CandidateCompany


class CandidateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateCompany
        fields = "__all__"
        depth = 1
