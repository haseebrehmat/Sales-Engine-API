from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from pseudos.models import Skills
from pseudos.serializers.skills import SkillSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class SkillView(ListAPIView):
    serializer_class = SkillSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id", "")
        return Skills.objects.filter(verticals_id=vertical_id)

    def post(self, request):
        serializer = SkillSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.validated_data["verticals_id"] = request.data.get("vertical_id")
            serializer.create(serializer.validated_data)
            message = "Skill created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class SkillDetailView(APIView):

    def get(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        serializer = SkillSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        request_data = request.data
        request_data["verticals_id"] = request.data.get("vertical_id")
        serializer = SkillSerializer(queryset, data=request_data)
        if serializer.is_valid():
            serializer.save()
            message = "Skill updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Skills.objects.filter(pk=pk).delete()
        return Response({"detail": "Skill deleted successfully"}, status=status.HTTP_200_OK)
