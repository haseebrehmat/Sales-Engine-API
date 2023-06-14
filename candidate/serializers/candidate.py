from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from authentication.models import User, Profile, Role
from candidate.models import Candidate, CandidateSkills, Skills, ExposedCandidate, SelectedCandidate, Designation
from rest_framework.exceptions import ValidationError


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField(default=[])
    designation = serializers.SerializerMethodField(default=[])
    allowed_status = serializers.SerializerMethodField(default=False)

    class Meta:
        model = Candidate
        fields = "__all__"
        depth = 1

    def get_skills(self, obj):
        queryset = CandidateSkills.objects.filter(candidate=obj)
        data = [x.skill.name for x in queryset]

        return data

    def get_designation(self, obj):
        return "" if obj.designation is None else obj.designation.title

    def get_allowed_status(self, obj):
        try:
            qs = SelectedCandidate.objects.filter(candidate=obj, company=self.context['request'].user.profile.company)
            return False if not qs.exists() else qs.first().status
        except Exception as e:
            print("Error => ", str(e))
            return False

    @transaction.atomic
    def create(self, validated_data):
        skills = validated_data.pop("skills")
        password = validated_data.pop("password")
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
        ExposedCandidate.objects.create(candidate=qs)
        try:
            user = User.objects.create(password=make_password(password), email=validated_data["email"])
            Profile.objects.create(user=user, company_id=validated_data["company_id"])
            user.roles = Role.objects.filter(name="candidate").first()
            user.save()
        except:
            raise ValidationError({ "detail" : "User already exist"}, code=406)

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
        designation = validated_data.get(
            "designation_id", instance.designation)
        instance.designation = Designation.objects.filter(id=designation).first()
        instance.save()
        CandidateSkills.objects.filter(candidate_id=instance.id).delete()
        data = [CandidateSkills(candidate_id=instance.id, skill_id=skill, level=1) for skill in skills]
        CandidateSkills.objects.bulk_create(data, ignore_conflicts=True)
        return instance
