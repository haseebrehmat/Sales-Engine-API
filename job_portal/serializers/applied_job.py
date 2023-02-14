import json
from collections import OrderedDict
from django.core import serializers as dj_serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from job_portal.models import JobDetail, AppliedJobStatus
from job_portal.serializers.job_detail import JobDetailSerializer, LinkSerializer


class AppliedJobDetailSerializer(serializers.Serializer):
    job_details = JobDetailSerializer()
    links = LinkSerializer(many=False, source='*')

    class Meta:
        fields = ['links', 'job_details', 'id']

    def to_representation(self, instance):
        # Here instance is instance of your model
        # so you can build your dict however you like
        result = OrderedDict()
        result['status'] = instance.job.job_status
        json_results = json.loads(dj_serializers.serialize("json", [instance.job]))[0]
        job_details = json_results['fields']
        job_details['id'] = json_results['pk']
        # result['job_details'] = job_details
        return job_details

class AppliedJobOuputSerializer(serializers.Serializer):
    data = AppliedJobDetailSerializer(many=True, source='*')
    links = LinkSerializer(many=False,source='*')

    class Meta:
        fields = ['links','data']

    def to_representation(self, instance):
        # Here instance is instance of your model
        # so you can build your dict however you like
        result = OrderedDict()
        result['status'] = instance.job.job_status
        result['job_id'] = instance.job.id
        return result


class JobStatusSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    status = serializers.IntegerField(required=True)

    class Meta:
        model = AppliedJobStatus
        fields = "__all__"

    errors = {}
    _errors = None
    validated_data = {}
    _validated_data = []

    def update(self, instance, validated_data):
        job_status = validated_data.pop('status')
        job_id = validated_data.pop('job')
        print(validated_data)

        job_details = JobDetail.objects.filter(id=job_id).update(job_status = job_status)
        obj = AppliedJobStatus.objects.get(job_id=job_id)
        return obj

    def is_valid(self, *args, **kwargs):
        # override drf.serializers.Serializer.is_valid
        # and raise CustomValidationErrors from parent validate
        self.validate(self.initial_data)
        return not bool(self.errors)

    def validate(self, attrs):

        self._errors = {}
        request = self.context.get('request', None)

        if attrs.get("status", None) == None and attrs.get("status", None) == 0:
            self._errors.update({"status":{"error": "Status is required between [0-6]","details": "Status is required between [1-6]"}})

        if attrs.get("job", None):
            job_id = attrs.get("job", None)
            job_status = attrs.get("status", None)
            applied_obj = AppliedJobStatus.objects.filter(job_id=job_id)

            if request.method == 'PATCH':
                pass
            elif applied_obj.count()>0:
                self._errors.update({"job_id":{"error": "This job is already applied","details": "This job is already applied"}})

        if len(self._errors):
            # set the overriden DRF values
            self.errors = self._errors
            # raise the sentinel error type
            raise ValidationError(self._errors)

        # set the overriden DRF serializer values
        self._errors = None
        self.validated_data = attrs
        self._validated_data = [[k, v] for k, v in attrs.items()]
        return attrs

    def create(self, validated_data):
        job_status = validated_data.pop('status')
        job_id = validated_data.pop('job')
        print(validated_data)

        job_details = JobDetail.objects.get(id=job_id)
        job_details.job_status = job_status
        job_details.save()
        obj = AppliedJobStatus.objects.create(job=job_details)
        obj.save()
        return obj

    def to_representation(self, instance):
        # Here instance is instance of your model
        # so you can build your dict however you like
        result = OrderedDict()
        result['status'] = instance.job.job_status
        result['job_id'] = instance.job.id
        return result