from rest_framework import serializers

from authentication.models import Profile, TeamRoleVerticalAssignment
from job_portal.models import JobDetail, AppliedJobStatus
from pseudos.models import Verticals


class JobDetailSerializer(serializers.ModelSerializer):
    job_status = serializers.CharField(default=0)
    total_vertical = serializers.SerializerMethodField(default=0)
    remaining_vertical = serializers.SerializerMethodField(default=0)

    class Meta:
        model = JobDetail
        exclude = [
            'job_description', 'job_description_tags', 'salary_max', 'salary_min', 'salary_format', 'estimated_salary'
        ]

    def get_total_vertical(self, obj):
        try:
            current_role_id = self.context['request'].user.roles_id
            verticals = TeamRoleVerticalAssignment.objects.filter(
                role_id=current_role_id, member=self.context['request'].user
            ).count()
        except:
            verticals = 0
        return verticals

    def get_remaining_vertical(self, obj):
        try:
            current_role_id = self.context['request'].user.roles_id
            # verticals = self.context['request'].user.profile.vertical.all()
            verticals = TeamRoleVerticalAssignment.objects.filter(
                role_id=current_role_id, member=self.context['request'].user
            ).values("vertical")
            used = AppliedJobStatus.objects.filter(job_id=obj.id, vertical__in=verticals).count()
            remaining = used
        except:
            remaining = 0
        return remaining


class JobKeywordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    count = serializers.IntegerField(default=0)


class LinkSerializer(serializers.Serializer):
    next = serializers.CharField(max_length=500)
    previous = serializers.CharField(max_length=500)


class TechKeywordSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    count = serializers.IntegerField(default=0)


class JobTypeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    count = serializers.IntegerField(default=0)


class JobDetailOutputSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=False, allow_null=True,
                                      format="%d-%m-%Y",
                                      input_formats=["%d-%m-%Y", "%Y-%m-%d"], )
    to_date = serializers.DateField(
        required=False, allow_null=True,
        format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "%Y-%m-%d"], )
    data = JobDetailSerializer(many=True, source='*')
    links = LinkSerializer(many=False, source='*')
    tech_keywords_count_list = TechKeywordSerializer(many=True, source='*')
    job_source_count_list = JobKeywordSerializer(many=True, source='*')
    job_type_count_list = JobTypeSerializer(many=True, source='*')

    class Meta:
        fields = ['links', 'job_source_count_list', 'data', 'tech_keywords_count_list', 'job_type_count_list']


class JobDataUploadSerializer(serializers.Serializer):
    file_upload = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False)
    )
    upload_by = serializers.CharField(max_length=500)


class SalesEngineJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = '__all__'