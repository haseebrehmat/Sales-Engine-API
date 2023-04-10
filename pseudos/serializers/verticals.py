from rest_framework import serializers

from pseudos.models import Verticals


class VerticalSerializer(serializers.ModelSerializer):
    hobbies = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Verticals
        fields = "__all__"


    def get_hobbies(self, obj):
        queryset = Verticals.objects.filter(id=obj.id).first()
        print("queryset => ", queryset.hobbies)
        if queryset is not None and queryset.hobbies is not None:
            return queryset.hobbies.split(",")
        else:
            return []
