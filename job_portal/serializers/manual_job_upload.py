from rest_framework import serializers
from job_portal.models import JobDetail
class ManualJobUploadSerializer(serializers.ModelSerializer):
    class Meta:
         model = JobDetail
         fields = '__all__'
    def create(self, validated_data):
        job_title = validated_data.get('job_title')
        company_name = validated_data.get('company_name')
        job_source = validated_data.get('job_source')
        job_type = validated_data.get('job_type')
        address = validated_data.get('address')
        job_description = validated_data.get('job_description')
        obj = JobDetail.objects.create(job_title=job_title.lower(),
                                       company_name=company_name.lower(),
                                       job_source=job_source.lower(),
                                       job_type=job_type.lower(),
                                       address=address.lower())
        return obj