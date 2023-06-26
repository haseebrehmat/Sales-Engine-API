from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.exceptions import InvalidUserException
from scraper.models import Accounts
from scraper.serializers.account import AccountSerializer
from settings.utils.helpers import serializer_errors

class AccountView(ListAPIView):
    serializer_class = AccountSerializer
    def get_queryset(self):
        return Accounts.objects.all()

    def post(self, request):
        conditions = [
            request.data.get("email", "") != "",
            request.data.get("password", "") != ""
        ]
        if all(conditions):
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                data = "Credentials Created Successfuly"
                status_code = status.HTTP_201_CREATED
                return Response({"detail": data}, status_code)
            else:
                data = serializer_errors(serializer)
                raise InvalidUserException(data)
        else:
            return Response({"detail": "Feilds cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
class AccountDetailView(APIView):
    def get(self, request, pk):
        obj = Accounts.objects.filter(pk=pk).first()
        if obj:
            serializer = AccountSerializer(obj, many=False)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Credential not available"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        conditions = [
            request.data.get("email", "") != "",
            request.data.get("password", "") != ""
        ]
        if all(conditions):
            queryset = Accounts.objects.filter(pk=pk).first()
            serializer = AccountSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                status_code = status.HTTP_200_OK
                message = {"detail": "Credentials updated successfully"}
                return Response(message, status=status_code)

            data = serializer_errors(serializer)
            raise InvalidUserException(data)
        else:
            return Response({"detail": "Feilds cannot be empty"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        Accounts.objects.filter(pk=pk).delete()
        message = {"detail": "Credential deleted successfully"}
        return Response(message, status=status.HTTP_200_OK)
