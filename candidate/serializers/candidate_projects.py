from rest_framework import serializers
from candidate.models import CandidateProjects


class CandidateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProjects
        fields = "__all__"
        depth = 1
    def update(self, instance, validated_data):
        proj = validated_data.pop("projects")
        cand = validated_data.pop("candidate")
        CandidateProjects.objects.filter(candidate_id=instance.id).delete()
        data = [CandidateProjects(candidate_id=cand.id, name=project["name"],
                                  description=project["description"], tags=project["tags"])
                for project in proj]
        CandidateProjects.objects.bulk_create(data, ignore_conflicts=True)
        return instance