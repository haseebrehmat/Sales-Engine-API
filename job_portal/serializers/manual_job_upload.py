from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from job_portal.models import JobDetail
from django.core.validators import URLValidator
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
        job_posted_date = validated_data.get('job_posted_date')
        job_source_url = validated_data.get('job_source_url')
        tech_keywords = validated_data.get('tech_keywords')
        is_manual = True
        obj = JobDetail.objects.create(job_title=job_title.lower(),
                                       company_name=company_name.lower(),
                                       job_source=job_source.lower(),
                                       job_type=job_type.lower(),
                                       address=address.lower(),
                                       job_description=job_description.lower(),
                                       job_posted_date=job_posted_date,
                                       job_source_url=job_source_url,
                                       tech_keywords=tech_keywords.lower(),
                                       is_manual=is_manual
                                       )
        return obj

    def validate_url_field(self, value):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except:
            return False
        return value