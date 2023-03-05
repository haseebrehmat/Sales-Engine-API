from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User, PasswordChangeLogs


class PasswordManagement(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if request.user.check_password(password):
            if new_password == "":
                message = "New password cannot be empty"
            elif request.data.get("old_password") == request.data.get("new_password"):
                message = "New password and current password cannot be same"
            else:
                user = User.objects.get(pk=request.user.pk)
                user.set_password(new_password)
                user.save()
                PasswordChangeLogs.objects.create(user_id=request.user.pk, password=make_password(password))
                message = "Password changed successfully"
                status_code = status.HTTP_200_OK
        else:
            message = "Your current password is not valid"

        return Response({'detail': message}, status_code)

