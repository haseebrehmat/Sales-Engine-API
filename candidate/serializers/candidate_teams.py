from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from candidate.models import CandidateTeam, ExposedCandidateTeam, ExposedCandidate


class CandidateTeamsSerializer(serializers.ModelSerializer):
    team_candidates = serializers.SerializerMethodField(default=[])
    class Meta:
        model = CandidateTeam
        fields = "__all__"
        depth = 1

    def get_team_candidates(self, obj):
        queryset = ExposedCandidateTeam.objects.filter(candidate_team=obj)
        data = [{'id': x.id, 'candidate': x.exposed_candidate.candidate.name} for x in queryset]
        return data

    def create(self, validated_data):
        exposed_candidates = validated_data.pop("exposed_candidates")
        if len(exposed_candidates) >= 2:
            try:
                candidate_team = CandidateTeam.objects.create(**validated_data)
            except Exception as e:
                raise ValidationError({"detail": e}, code=406)
        else:
            raise ValidationError({"detail": "Please select more than one candidate"}, code=406)
        data = [ExposedCandidateTeam(candidate_team=candidate_team,
                                     exposed_candidate=ExposedCandidate.objects.filter(pk=exposed_candidate).first())
                for exposed_candidate in exposed_candidates]
        ExposedCandidateTeam.objects.bulk_create(data, ignore_conflicts=True)

    def update(self, instance, validated_data):
        exposed_candidates_ids = validated_data.pop("exposed_candidates", "")



        candidate_team_id = instance.id
        instance.name = validated_data.get("name", instance.name)
        try:
            instance.save()
        except Exception as e:
            raise ValidationError({"detail": e}, code=406)
        ExposedCandidateTeam.objects.filter(candidate_team_id=candidate_team_id).delete()
        data = [ExposedCandidateTeam(candidate_team=instance,
                                     exposed_candidate=ExposedCandidate.objects.filter(pk=exposed_candidate).first())
                for exposed_candidate in exposed_candidates_ids]
        ExposedCandidateTeam.objects.bulk_create(data, ignore_conflicts=True)
        return instance

