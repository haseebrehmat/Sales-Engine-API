from rest_framework import serializers

from job_portal.models import JobDetail

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = "__all__"

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
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],)
    to_date = serializers.DateField(
        required=False, allow_null=True,
        format="%d-%m-%Y",
        input_formats=["%d-%m-%Y", "%Y-%m-%d"],)
    data = JobDetailSerializer(many=True, source='*')
    links = LinkSerializer(many=False,source='*')
    tech_keywords_count_list = TechKeywordSerializer(many=True,source='*')
    job_source_count_list = JobKeywordSerializer(many=True,source='*')
    job_type_count_list = JobTypeSerializer(many=True,source='*')

    class Meta:
        fields = ['links','job_source_count_list','data','tech_keywords_count_list','job_type_count_list']



class JobDataUploadSerializer(serializers.Serializer):
    file_upload = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False)
    )
    upload_by = serializers.CharField(max_length=500)