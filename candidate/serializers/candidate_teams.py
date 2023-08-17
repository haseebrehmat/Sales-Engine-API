from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models.company import Company
from candidate.models import CandidateTeam, ExposedCandidateTeam, ExposedCandidate
from django.db import transaction



class CandidateTeamsSerializer(serializers.ModelSerializer):
    team_candidates = serializers.SerializerMethodField(default=[])
    exposed_to_companies = serializers.SerializerMethodField(default=[])
    class Meta:
        model = CandidateTeam
        fields = "__all__"
        depth = 1

    def get_team_candidates(self, obj):
        data = []
        queryset = ExposedCandidateTeam.objects.filter(candidate_team=obj)
        data = [{'id': x.exposed_candidate_id, 'candidate': x.exposed_candidate.candidate.name} for x in queryset]
        return data
    def get_exposed_to_companies(self, obj):
        data = []
        if obj.exposed_to:
            temp_data = Company.objects.filter(id__in=obj.exposed_to)
            data = [{"id": x.id, "name": x.name} for x in temp_data]
        return data

    @transaction.atomic
    def create(self, validated_data):
        exposed_candidates = validated_data.pop("exposed_candidates")
        # verify exposed candidates lists, it should not add invalid exposed candidate if not exist, if possible show error
        [self.check_exposed_candidate(x) for x in exposed_candidates]

        if len(exposed_candidates) >= 2:
            try:
                candidate_team = CandidateTeam.objects.create(**validated_data)
            except Exception as e:
                if "duplicate key value violates unique constraint" in str(e):
                    raise ValidationError({"detail": "Team Already Exist"}, code=406)
                else:
                    raise ValidationError({"detail": e}, code=406)
        else:
            raise ValidationError({"detail": "Please select more than one candidate"}, code=406)
        data = [ExposedCandidateTeam(candidate_team=candidate_team,
                                     exposed_candidate_id=exposed_candidate)
                for exposed_candidate in exposed_candidates]
        ExposedCandidateTeam.objects.bulk_create(data, ignore_conflicts=True)

    @transaction.atomic
    def update(self, instance, validated_data):
        exposed_candidates_ids = validated_data.pop("exposed_candidates", "")
        # verify exposed candidates lists, it should not add invalid exposed candidate if not exist, if possible show error

        [self.check_exposed_candidate(x) for x in exposed_candidates_ids]
        candidate_team_id = instance.id
        instance.name = validated_data.get("name", instance.name)
        try:
            instance.save()
        except Exception as e:
            raise ValidationError({"detail": e}, code=406)
        ExposedCandidateTeam.objects.filter(candidate_team_id=candidate_team_id).delete()
        data = [ExposedCandidateTeam(candidate_team=instance,
                                     exposed_candidate_id=exposed_candidate)
                for exposed_candidate in exposed_candidates_ids]
        ExposedCandidateTeam.objects.bulk_create(data, ignore_conflicts=True)
        return instance
    def check_exposed_candidate(self,id):
        obj = ExposedCandidate.objects.filter(pk=id).first()
        if obj is None:
            raise ValidationError({"detail": f"Exposed Candidate not found"}, code=406)


