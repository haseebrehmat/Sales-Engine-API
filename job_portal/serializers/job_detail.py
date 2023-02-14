from rest_framework import serializers

from apps.db_api.models import JobDetailsModel

JOB_STATUS_CHOICE = [
    (0,'To Apply'),
    (1, 'Applied'),
    (2,'Hired'),
    (3, 'Rejected'),
    (4, 'Warm Lead'),
    (5,'Hot Lead'),
]

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetailsModel
        fields = "__all__"

class JobKeywordsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    count = serializers.IntegerField(default=0)

class LinksSerializer(serializers.Serializer):
    next = serializers.CharField(max_length=500)
    previous = serializers.CharField(max_length=500)

class TechKeywordsSerializer(serializers.Serializer):
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
    links = LinksSerializer(many=False,source='*')
    tech_keywords_count_list = TechKeywordsSerializer(many=True,source='*')
    job_source_count_list = JobKeywordsSerializer(many=True,source='*')
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