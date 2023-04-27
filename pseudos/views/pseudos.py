from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

from authentication.exceptions import InvalidUserException
from pseudos.models import Pseudos
from pseudos.permissions.pseudos import PseudoPermissions
from pseudos.serializers.pseudos import PseudoSerializer
from pseudos.utils.custom_pagination import CustomPagination
from settings.utils.helpers import serializer_errors


class PseudosView(ListAPIView):
    permission_classes = (PseudoPermissions,)
    serializer_class = PseudoSerializer
    pagination_class = CustomPagination
    queryset = Pseudos.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        return self.queryset.filter(company=self.request.user.profile.company)

    def post(self, request):
        serializer = PseudoSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.validated_data["company_id"] = request.user.profile.company.id
            serializer.create(serializer.validated_data)
            message = "Pseudo created successfully"
            status_code = status.HTTP_201_CREATED
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)


class PseudoDetailView(APIView):
    permission_classes = (PseudoPermissions,)

    def get(self, request, pk):
        queryset = Pseudos.objects.filter(pk=pk).first()
        serializer = PseudoSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        queryset = Pseudos.objects.filter(pk=pk).first()
        serializer = PseudoSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Pseudo updated successfully"
            status_code = status.HTTP_200_OK
            return Response({"detail": message}, status_code)
        else:
            data = serializer_errors(serializer)
            raise InvalidUserException(data)

    def delete(self, request, pk):
        Pseudos.objects.filter(pk=pk).delete()
        return Response({"detail": "Pseudo deleted successfully"}, status=status.HTTP_200_OK)
