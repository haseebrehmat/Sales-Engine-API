import uuid
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User, PasswordChangeLogs, ResetPassword


class PasswordReset(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        email = request.GET.get("email")
        if email is None:
            message = "Email cannot be empty"
        else:
            try:
                user = User.objects.get(email=email)
                reset_code = uuid.uuid4
                ResetPassword.objects.filter(user_id=user.id, reset_code=reset_code)
                status_code = status.HTTP_200_OK
                message = "Reset link generated, Check your email"
            except User.DoesNotExist:
                message = "Email not found"
        return Response(message, status_code)

    def post(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        password = request.data.get("new_password")
        try:
            queryset = ResetPassword.objects.get(reset_code=request.data.get("reset_code"))
            expiry_time = queryset.created_at + timedelta(hours=24)
            current_time = datetime.now()
            if current_time < expiry_time:
                user = User.objects.get(pk=queryset.user.pk)
                user.set_password(password)
                user.save()
                PasswordChangeLogs.objects.create(user_id=request.user.pk, password=make_password(password))
                message = "Password changed successfully"
                status_code = status.HTTP_200_OK
            else:
                message = "Reset link expired"
        except ResetPassword.DoesNotExist:
            message = "Invalid url"

        return Response(message, status_code)

