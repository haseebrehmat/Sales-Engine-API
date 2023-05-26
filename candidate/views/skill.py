from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models import Skills
from candidate.serializers.skills import SkillsSerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class SkillsListView(ListAPIView):
    serializer_class = SkillsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Skills.objects.all()
        return queryset

    def post(self, request):
        serializer = SkillsSerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.create(data)
            message = "Skills created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)


class SkillsDetailView(APIView):

    def get(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        data = []
        if queryset is not None:
            serializer = SkillsSerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        serializer = SkillsSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.profile.company.id)
            message = "Skills updated successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

    def delete(self, request, pk):
        Skills.objects.filter(pk=pk).delete()
        return Response({"detail": "Skills deleted successfully"}, status.HTTP_200_OK)





