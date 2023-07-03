from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from authentication.models import User, Profile, Role
from candidate.models import Candidate, CandidateSkills, Skills, ExposedCandidate, SelectedCandidate, Designation, \
    CandidateTools, Tools, Regions, CandidateRegions, CandidateProjects
from rest_framework.exceptions import ValidationError


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField(default=[])
    designation = serializers.SerializerMethodField(default=[])
    tools = serializers.SerializerMethodField(default=[])
    regions = serializers.SerializerMethodField(default=[])
    allowed_status = serializers.SerializerMethodField(default=False)

    class Meta:
        model = Candidate
        fields = "__all__"
        depth = 1

    def get_skills(self, obj):
        queryset = CandidateSkills.objects.filter(candidate=obj)
        data = [{'name': x.skill.name, 'level': x.level} for x in queryset]
        return data

    def get_regions(self, obj):
        queryset = CandidateRegions.objects.filter(candidate=obj)
        data = [{"id": x.region.id, "name": x.region.region} for x in queryset]
        return data

    def get_tools(self, obj):
        queryset = CandidateTools.objects.filter(candidate=obj)
        data = [{'tool': x.tool.name, 'description': x.tool.description} for x in queryset]
        return data

    def get_designation(self, obj):
        return "" if obj.designation is None else {"id": obj.designation.id, "name": obj.designation.title,
                                                   "description": obj.designation.description}

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
        tools = validated_data.pop("tools")
        regions = validated_data.pop("regions")
        password = validated_data.pop("password")
        if Candidate.objects.filter(company_id=validated_data["company_id"], email=validated_data["email"]).exists():
            raise ValidationError({"detail": "User already exist"}, code=406)
        temp = []
        temp_level = []
        for skill in skills:
            name = skill['name']
            level = skill['level']
            qs = Skills.objects.filter(name__iexact=name).first()
            if qs:
                temp.append(qs.id)
                temp_level.append(level)
            else:
                qs = Skills.objects.create(name=name.lower())
                temp.append(qs.id)
                temp_level.append(level)
        skills = temp
        temp = []
        for region in regions:
            re = region["label"]
            print(re)
            qs = Regions.objects.filter(region__iexact=re).first()
            if qs:
                temp.append(qs.id)
            else:
                qs = Regions.objects.create(region=re.lower())
                temp.append(qs.id)
        regions = temp
        temp = []
        for tool in tools:
            name = tool['tool']
            description = tool['description']
            qs = Tools.objects.filter(name__iexact=name).first()
            if qs:
                qs.description = description
                qs.save()
                temp.append(qs.id)
            else:
                qs = Tools.objects.create(name=name.lower(), description=description)
                temp.append(qs.id)
        tools = temp
        qs = Candidate.objects.create(**validated_data)
        data = [CandidateSkills(candidate_id=qs.id, skill_id=skill, level=temp_level[position]) for position, skill in enumerate(skills)]
        CandidateSkills.objects.bulk_create(data, ignore_conflicts=True)
        data = [CandidateTools(candidate_id=qs.id, tool_id=tool) for tool in tools]
        CandidateTools.objects.bulk_create(data, ignore_conflicts=True)
        data = [CandidateRegions(candidate_id=qs.id, region_id=region) for region in regions]
        CandidateRegions.objects.bulk_create(data, ignore_conflicts=True)
        if not User.objects.filter(password=make_password(password), email=validated_data["email"]).exists():
            user = User.objects.create(password=make_password(password), email=validated_data["email"])
            Profile.objects.create(user=user, company_id=validated_data["company_id"])
            user.roles = Role.objects.filter(name="candidate").first()
            user.save()
        else:
            print("User Already Exit")

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills")
        tools = validated_data.pop("tools")
        regions = validated_data.pop("regions")
        temp = []
        for tool in tools:
            name = tool['tool']
            description = tool['description']
            qs = Tools.objects.filter(name__iexact=name).first()
            if qs:
                qs.description = description
                qs.save()
                temp.append(qs.id)
            else:
                qs = Tools.objects.create(name=name.lower(), description=description)
                temp.append(qs.id)
        tools = temp
        temp = []
        temp_level = []
        for skill in skills:
            name = skill['name']
            level = skill['level']
            qs = Skills.objects.filter(name__iexact=name).first()
            if qs:
                temp.append(qs.id)
                temp_level.append(level)
            else:
                qs = Skills.objects.create(name=name.lower())
                temp.append(qs.id)
                temp_level.append(level)
        skills = temp
        temp = []
        for region in regions:
            re = region["label"]
            qs = Regions.objects.filter(region__iexact=re).first()
            if qs:
                temp.append(qs.id)
            else:
                qs = Regions.objects.create(region=re.lower())
                temp.append(qs.id)
        regions = temp
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
        CandidateTools.objects.filter(candidate_id=instance.id).delete()
        CandidateRegions.objects.filter(candidate_id=instance.id).delete()

        data = [CandidateSkills(candidate_id=instance.id, skill_id=skill, level=temp_level[position]) for position, skill in
                enumerate(skills)]
        CandidateSkills.objects.bulk_create(data, ignore_conflicts=True)
        data = [CandidateTools(candidate_id=instance.id, tool_id=tool) for tool in tools]
        CandidateTools.objects.bulk_create(data, ignore_conflicts=True)
        data = [CandidateRegions(candidate_id=instance.id, region_id=re) for re in regions]
        CandidateRegions.objects.bulk_create(data, ignore_conflicts=True)
        return instance






