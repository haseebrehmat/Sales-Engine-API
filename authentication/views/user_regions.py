from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from authentication.models.user_regions import UserRegions
from authentication.serializers.user_regions import UserRegionsSerializer


class UserRegionsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRegionsSerializer

    def get_queryset(self):
        queryset = UserRegions.objects.all()
        return queryset
