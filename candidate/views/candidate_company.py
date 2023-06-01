from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import InvalidUserException
from candidate.models.candidate_company import CandidateCompany
from candidate.serializers.candidate_company import CandidateCompanySerializer
from settings.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors

class CandidateCompanyListView(ListAPIView):

    serializer_class = CandidateCompanySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = CandidateCompany.objects.all()
        return queryset

    def post(self, request):
        serializer = CandidateCompanySerializer(data=request.data, many=False)
        if serializer.is_valid():
            data = serializer.validated_data
            data["company_id"] = request.user.profile.company.id
            data["candidate_id"] = request.data["candidate_id"]
            try:
              if not CandidateCompany.objects.filter(company_id=data["company_id"], candidate_id=data["candidate_id"]).exists():
                serializer.create(data)
                message = "Candidate with this company created successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
              else:
                message = "Candidate with this company already exist"
                status_code = status.HTTP_404_NOT_FOUND
                return Response({"detail": message}, status_code)
            except Exception as e:
              message = "No candidate with this company found"
              status_code = status.HTTP_404_NOT_FOUND
              return Response({"detail": message}, status_code)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

class CandidateCompanyDetailView(APIView):

    def get(self, request, pk):
        queryset = CandidateCompany.objects.filter(pk=pk).first()
        data = []
        if queryset is not None:
            serializer = CandidateCompanySerializer(queryset, many=False)
            data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = CandidateCompany.objects.filter(pk=pk).first()
        serializer = CandidateCompanySerializer(instance=queryset, data=request.data)
        if queryset:
          try:
            if serializer.is_valid():
              if not CandidateCompany.objects.filter(company_id=request.user.profile.company.id, candidate_id=request.data['candidate_id']).exists():
                serializer.save(company_id=request.user.profile.company.id, candidate_id=request.data['candidate_id'])
                message = "Candidate with this company updated successfully"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": message}, status_code)
              else:
                message = "No changes were made"
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                return Response({"detail": message}, status_code)

          except Exception as e:
            return e

        else:
          message = "No candidate with this company found"
          status_code = status.HTTP_404_NOT_FOUND
          return Response({"detail": message}, status_code)

        data = serializer_errors(serializer)
        raise InvalidUserException(data)


    def delete(self, request, pk):
        CandidateCompany.objects.filter(pk=pk).delete()
        return Response({"detail": "Candidate deleted successfully"}, status.HTTP_200_OK)
