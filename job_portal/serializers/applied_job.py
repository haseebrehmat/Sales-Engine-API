import json
from collections import OrderedDict
from django.core import serializers as dj_serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from job_portal.models import JobDetail, AppliedJobStatus
from job_portal.serializers.job_detail import JobDetailSerializer, LinkSerializer


class AppliedJobDetailSerializer(serializers.Serializer):
    job_details = JobDetailSerializer()
    links = LinkSerializer(many=False, source='*')

    class Meta:
        fields = ['links', 'job_details', 'id']

    def to_representation(self, instance):
        # Here instance is instance of your model
        result = OrderedDict()

        json_results = json.loads(dj_serializers.serialize("json", [instance.job]))[0]
        job_details = json_results['fields']
        job_details['id'] = json_results['pk']
        job_details['applied_job_id'] = instance.id
        job_details['applied_date'] = instance.applied_date
        job_details['status'] = instance.job_status
        job_details['is_converted'] = instance.is_converted
        job_details['converted_at'] = instance.converted_at
        try:
            job_details["resume"] = instance.resume
            job_details["vertical"] = {"id": instance.vertical.id, "name": instance.vertical.name,
                                       "identity": instance.vertical.identity, "pseudo": instance.vertical.pseudo.name}
            job_details["cover_letter"] = instance.cover_letter
        except Exception as e:
            print(e)

        # result['job_details'] = job_details
        return job_details


class TeamAppliedJobDetailSerializer(serializers.Serializer):
    job_details = JobDetailSerializer()
    links = LinkSerializer(many=False, source='*')

    class Meta:
        fields = ['links', 'job_details']

    def to_representation(self, instance):
        # Here instance is instance of your model
        result = OrderedDict()
        json_results = json.loads(dj_serializers.serialize("json", [instance.job]))[0]
        job_details = json_results['fields']
        job_details['id'] = instance.pk
        job_details['applied_by'] = instance.applied_by.pk
        job_details['applied_by_name'] = instance.applied_by.username
        job_details['status'] = instance.job_status
        job_details['applied_date'] = instance.applied_date
        job_details['is_converted'] = instance.is_converted

        try:
            job_details['job_source'] = instance.job.job_source
            job_details['tech_stack'] = instance.job.tech_keywords
            job_details['job_type'] = instance.job.job_type
        except Exception as e:
            print("Exception in applied job serializer", e)

        try:
            job_details["resume"] = instance.resume
            job_details["vertical"] = {"id": instance.vertical.id, "name": instance.vertical.name,
                                       "identity": instance.vertical.identity}
            job_details['pseudo'] = {
                "name": instance.vertical.pseudo.name
            }
            job_details["cover_letter"] = instance.cover_letter
        except Exception as e:
            print(e)

        # result['job_details'] = job_details
        return job_details


class AppliedJobOuputSerializer(serializers.Serializer):
    data = AppliedJobDetailSerializer(many=True, source='*')
    links = LinkSerializer(many=False, source='*')

    class Meta:
        fields = ['links', 'data']

    def to_representation(self, instance):
        # Here instance is instance of your model
        # so you build your dict however you like
        result = OrderedDict()
        result['status'] = instance.job_status
        result['job_id'] = instance.id
        return result


class JobStatusSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    applied_by = serializers.UUIDField(read_only=True)

    class Meta:
        model = AppliedJobStatus
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     job_status = validated_data.pop('status')
    #     job_id = validated_data.pop('job')
    #     print(validated_data)
    #
    #     job_details = JobDetail.objects.filter(id=job_id).update(job_status = job_status)
    #     obj = AppliedJobStatus.objects.get(job_id=job_id)
    #     return obj

    # def create(self, validated_data):
    #     job_status = validated_data.pop('status')
    #     job_id = validated_data.pop('job')
    #     # print(validated_data)
    #
    #     job_details = JobDetail.objects.get(id=job_id)
    #     job_details.job_status = job_status
    #     job_details.save()
    #     obj = AppliedJobStatus.objects.create(job=job_details)
    #     obj.save()
    #     return obj

    def to_representation(self, instance):
        # Here instance is instance of your model
        result = OrderedDict()
        result['status'] = instance.job_status
        result['job_id'] = instance.id
        return result
