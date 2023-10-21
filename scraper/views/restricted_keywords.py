from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.exceptions import InvalidUserException
from scraper.models import RestrictedJobsTags
from scraper.serializers.restricted_tags import RestrictedTagsSerializer
from settings.utils.helpers import serializer_errors


class RestrictedJobTagsView(ListAPIView):
    serializer_class = RestrictedTagsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return RestrictedJobsTags.objects.all()

    def post(self, request):
        if type(request.data) == dict:
            many = False
        else:
            many = True
        serializer = RestrictedTagsSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            data = "Keywords Created Successfuly"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": data}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class RestrictedJobTagsDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        obj = RestrictedJobsTags.objects.filter(pk=pk).first()
        if obj:
            serializer = RestrictedTagsSerializer(obj, many=False)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Keyword not available"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        queryset = RestrictedJobsTags.objects.filter(pk=pk).first()
        serializer = RestrictedTagsSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            message = {"detail": "Keywords updated successfully"}
            return Response(message, status=status_code)

        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        RestrictedJobsTags.objects.filter(pk=pk).delete()
        message = {"detail": "Keyword deleted successfully"}
        return Response(message, status=status.HTTP_200_OK)
