from rest_framework import serializers

from pseudos.models import Verticals, VerticalsRegions


class VerticalSerializer(serializers.ModelSerializer):
    hobbies = serializers.SerializerMethodField(default=[])
    regions = serializers.SerializerMethodField(default=[])
    class Meta:
        model = Verticals
        fields = "__all__"
        depth = 1

    def get_hobbies(self, obj):
        queryset = Verticals.objects.filter(id=obj.id).first()
        if queryset is not None and queryset.hobbies is not None:
            return queryset.hobbies.split(",")
        else:
            return []

    def get_regions(self, obj):
        vertical_regions = [{'label': vertical_regions.region.region, 'value': vertical_regions.region.id} for
                            vertical_regions in VerticalsRegions.objects.filter(verticals=obj)]
        return vertical_regions
