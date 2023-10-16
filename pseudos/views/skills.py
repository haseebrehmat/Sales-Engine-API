from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from pseudos.models import Skills, GenericSkills
from pseudos.permissions.generic_skills import GenericSkillsPermissions
from pseudos.permissions.verticals import VerticalPermissions
from pseudos.serializers.skills import SkillSerializer, GenericSkillSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class SkillView(ListAPIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = SkillSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        vertical_id = self.request.GET.get("id")
        return Skills.objects.filter(vertical_id=vertical_id).exclude(vertical_id=None)

    def post(self, request):
        serializer = SkillSerializer(data=request.data, many=False)
        if serializer.is_valid():
            try:
                serializer.validated_data["vertical_id"] = request.data.get("vertical_id")
                serializer.validated_data["generic_skill_id"] = request.data.get("generic_skill_id")
                serializer.create(serializer.validated_data)
                message = "Skill added successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Skill already exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class SkillDetailView(APIView):
    permission_classes = (VerticalPermissions,)
    serializer_class = SkillSerializer
    def get(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        serializer = SkillSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Skills.objects.filter(pk=pk).first()
        request_data = request.data
        print(request.data.get("generic_skill_id"))
        skill = GenericSkills.objects.filter(id=request.data.get("generic_skill_id"))
        print(skill)
        request_data["generic_skill"] = skill
        serializer = SkillSerializer(queryset, data=request_data)
        if serializer.is_valid():
            try:
                serializer.save(generic_skill_id=request.data.get("generic_skill_id"))
                message = "Skill updated successfully"
                status_code = status.HTTP_200_OK
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Skill already exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Skills.objects.filter(pk=pk).delete()
        return Response({"detail": "Skill deleted successfully"}, status=status.HTTP_200_OK)


# Add these new classes for generic skills for company based

class GenericSkillView(ListAPIView):
    permission_classes = (GenericSkillsPermissions,)
    serializer_class = GenericSkillSerializer
    pagination_class = CustomPagination
    GENERIC_SKILL_TYPES = {
            'clientside': 'Client Side',
            'serverside': 'Server Side',
            'devops': 'DevOps',
            'others': 'Others',
        }

    def get_queryset(self):
        queryset = GenericSkills.objects.filter(company_id=self.request.user.profile.company_id).exclude(company_id=None)
        search = self.request.GET.get("search", "")
        if search != "":
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def post(self, request):
        conditions = [
            request.data.get("name", "") != "",
            request.data.get("type", "") != "",
        ]
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.data.get('type') not in self.GENERIC_SKILL_TYPES:
            return Response({"detail": "Skill type is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = GenericSkillSerializer(data=request.data, many=False)
        if serializer.is_valid():
            try:
                serializer.validated_data["company_id"] = self.request.user.profile.company_id
                serializer.create(serializer.validated_data)
                message = "Skill created successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Skill with same name and type is already existed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class GenericSkillDetailView(APIView):
    permission_classes = (GenericSkillsPermissions,)
    GENERIC_SKILL_TYPES = {
        'clientside': 'Client Side',
        'serverside': 'Server Side',
        'devops': 'DevOps',
        'others': 'Others',
    }

    def get(self, request, pk):
        queryset = GenericSkills.objects.filter(pk=pk).first()
        serializer = GenericSkillSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = GenericSkills.objects.filter(pk=pk).first()
        if request.data.get('type') not in self.GENERIC_SKILL_TYPES:
            return Response({"detail": "Skill type is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        request_data = request.data
        serializer = GenericSkillSerializer(queryset, data=request_data)
        if serializer.is_valid():
            try:
                serializer.save()
                message = "Generic Skill updated successfully"
                status_code = status.HTTP_200_OK
                return Response({"detail": message}, status_code)
            except Exception as e:
                return Response({"detail": "Skill with same name and type is already existed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        GenericSkills.objects.filter(pk=pk).delete()
        return Response({"detail": "Generic Skill deleted successfully"}, status=status.HTTP_200_OK)



