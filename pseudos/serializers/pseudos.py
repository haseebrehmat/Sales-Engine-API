from rest_framework import serializers

from pseudos.models import Pseudos, Verticals


class PseudoSerializer(serializers.ModelSerializer):
    verticals = serializers.SerializerMethodField(default=[])

    class Meta:
        model = Pseudos
        fields = "__all__"

    def get_verticals(self, obj):
        queryset = Verticals.objects.filter(pseudo=obj)
        return [{"id": x.id, "name": x.name} for x in queryset]
