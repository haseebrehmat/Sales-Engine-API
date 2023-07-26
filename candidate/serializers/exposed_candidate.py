from rest_framework import serializers

from authentication.models.company import Company
from candidate.models import ExposedCandidate, CandidateSkills


class ExposedCandidateSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField(default=None, write_only=True)
    company_id = serializers.UUIDField(default=None)
    # company = serializers.IntegerField(write_only=False)
    exposed_to = serializers.SerializerMethodField(default=[], read_only=True)
    candidate = serializers.SerializerMethodField(default={}, read_only=True)

    class Meta:
        model = ExposedCandidate
        fields = "__all__"
        # depth = 1

    def get_exposed_to(self, obj):
        queryset = ExposedCandidate.objects.filter(candidate_id=obj.candidate_id)
        try:
            return [
                {
                    "id": x.company.id,
                    "name": x.company.name,
                    "exposed_candidate_id": x.id
                } for x in queryset if x.id is not None and x.company is not None
            ]
        except Exception as e:
            return []

    def get_candidate(self, obj):
        data = {
            "id": obj.candidate.id,
            "name": obj.candidate.name,
            "email": obj.candidate.email,
            "designation": "" if obj.candidate.designation is None else obj.candidate.designation.title
        }
        queryset = CandidateSkills.objects.filter(candidate=obj.candidate)
        data['skills'] = [x.skill.name for x in queryset]

        return data

    def create(self, validated_data):
        ExposedCandidate.objects.create(**validated_data)
