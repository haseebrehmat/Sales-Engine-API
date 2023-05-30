from rest_framework import serializers

from candidate.models import Candidate, CandidateSkills, Skills


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Candidate
        fields = "__all__"
        depth = 1

    def get_skills(self, obj):
        queryset = CandidateSkills.objects.filter(candidate=obj)
        data = [x.skill.name for x in queryset]

        return data

    def create(self, validated_data):
        skills = validated_data.pop("skills")
        temp = []
        for skill in skills:
            qs = Skills.objects.filter(name__iexact=skill).first()
            if qs:
                temp.append(qs.id)
            else:
                qs = Skills.objects.create(name=skill.lower())
                temp.append(qs.id)
        skills = temp

        qs = Candidate.objects.create(**validated_data)
        data = [CandidateSkills(candidate_id=qs.id, skill_id=skill, level=1) for skill in skills]
        CandidateSkills.objects.bulk_create(data, ignore_conflicts=True)

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills")
        temp = []
        for skill in skills:
            qs = Skills.objects.filter(name__iexact=skill).first()
            if qs:
                temp.append(qs.id)
            else:
                qs = Skills.objects.create(name=skill.lower())
                temp.append(qs.id)
        skills = temp

        instance.employee_id = validated_data.get(
            "employee_id", instance.employee_id)
        instance.name = validated_data.get("name", instance.name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.experience = validated_data.get(
            "experience", instance.experience)
        instance.email = validated_data.get("email", instance.email)
        instance.designation = validated_data.get(
            "designation", instance.designation)
        instance.save()
        print(skills)
        CandidateSkills.objects.filter(candidate_id=instance.id).delete()
        data = [CandidateSkills(candidate_id=instance.id, skill_id=skill, level=1) for skill in skills]
        CandidateSkills.objects.bulk_create(data, ignore_conflicts=True)
        return instance
