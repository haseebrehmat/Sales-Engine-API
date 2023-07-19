from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from authentication.models import UserRegions, User
from pseudos.models import Verticals, VerticalsRegions
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.verticals import VerticalSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class VerticalView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = VerticalSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Verticals.objects.filter(pseudo_id=self.request.GET.get("pseudo_id")).exclude(pseudo_id=None)
        return queryset

    def post(self, request):
        request_data = request.data
        request_data["hobbies"] = request_data.get("hobbies", "")
        if request_data["hobbies"] != "":
            request_data["hobbies"] = ",".join(request_data["hobbies"])

        serializer = VerticalSerializer(data=request_data, many=False)

        if serializer.is_valid():
            serializer.validated_data["pseudo_id"] = request.data.get("pseudo_id")
            serializer.create(serializer.validated_data)
            message = "Vertical created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class VerticalDetailView(APIView):
    permission_classes = (VerticalPermissions,)

    def get(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        serializer = VerticalSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        queryset = Verticals.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["pseudo_id"] = request_data.get("pseudo_id")
        request_data["hobbies"] = request_data.get("hobbies", "")
        regions = request_data.pop("regions")
        if request_data["hobbies"] != "":
            request_data["hobbies"] = ",".join(request_data["hobbies"])
        print(request_data["hobbies"])
        serializer = VerticalSerializer(queryset, data=request_data)
        if serializer.is_valid():
            VerticalsRegions.objects.filter(verticals=queryset).delete()
            verticals_regions_data =[VerticalsRegions(verticals=queryset, region_id=region) for region in regions]
            VerticalsRegions.objects.bulk_create(verticals_regions_data)
            serializer.save(hobbies=request_data["hobbies"])
            # revalidate user verticals
            users = User.objects.filter(profile__vertical=queryset)
            for user in users:
                if not self.is_valid_vertical(queryset, user):
                    user.profile.vertical.remove(queryset)
            message = "Vertical updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Verticals.objects.filter(pk=pk).delete()
        return Response({"detail": "Verticals deleted successfully"}, status=status.HTTP_200_OK)

    def is_valid_vertical(self, vertical, user):
        verticals_regions_set = set(
            VerticalsRegions.objects.filter(verticals=vertical).values_list('region', flat=True))
        user_regions_set = set(UserRegions.objects.filter(user=user).values_list('region', flat=True))
        result = verticals_regions_set.intersection(user_regions_set)
        return True if result else False