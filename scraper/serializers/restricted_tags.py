from rest_framework.serializers import ModelSerializer

from scraper.models import RestrictedJobsTags


class RestrictedTagsSerializer(ModelSerializer):

    class Meta:
        model = RestrictedJobsTags
        fields = '__all__'

