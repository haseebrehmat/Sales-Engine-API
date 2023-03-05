import re
import uuid
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User, PasswordChangeLogs, ResetPassword
from django.core.mail import EmailMultiAlternatives
from settings.base import FROM_EMAIL
from settings.utils.helpers import validate_password


class PasswordReset(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        email = request.GET.get("email")
        if email is None:
            message = {"detail": "Email cannot be empty"}
        else:
            try:
                user = User.objects.get(email=email)
                reset_code = uuid.uuid1().hex[:10]  # generating uuid upto 10 digits
                try:
                    # if entry exist
                    queryset = ResetPassword.objects.get(user_id=user.id)
                    queryset.reset_code = reset_code
                    queryset.status = False
                    queryset.save()
                except ResetPassword.DoesNotExist:
                    ResetPassword.objects.create(user_id=user.id, reset_code=reset_code)

                status_code = status.HTTP_200_OK
                message = {"detail": "Reset link generated, Check your email"}
                context = {
                    "browser": request.META.get("HTTP_USER_AGENT", "Not Available"),        # getting browser name
                    "username": user.username,
                    "company": "Octagon",
                    "operating_system": request.META.get("GDMSESSION", "Not Available"),    # getting os name
                    "reset_url": f"http:10.10.8.229:8000/api/auth/reset/{user.email}/{reset_code}"
                }

                # rendering context in email template and converting it into string
                html_string = render_to_string("emails/forgot_password.html", context)
                msg = EmailMultiAlternatives("Reset Password", "Reset Password",
                                             FROM_EMAIL,
                                             [user.email])

                msg.attach_alternative(
                    html_string,
                    "text/html"
                )
                email_status = msg.send()
                print(email_status)
            except User.DoesNotExist:
                message = {"detail": "Email not found"}
        return Response(message, status_code)

    def post(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if password != "":
            if password == confirm_password:
                if validate_password(password):
                    try:
                        queryset = ResetPassword.objects.get(reset_code=request.data.get("code"))
                        if queryset.status:
                            message = "Password already changed"
                        else:
                            user = User.objects.get(pk=queryset.user.pk)
                            user.set_password(password)
                            user.save()
                            queryset.status = True
                            queryset.save()
                            PasswordChangeLogs.objects.create(user_id=user.pk, password=make_password(password))
                            message = "Password updated successfully"
                            status_code = status.HTTP_200_OK

                    except ResetPassword.DoesNotExist:
                        message = "Reset code not found"
                else:
                    message = "Please choose strong password"
            else:
                message = "Password didn't match"
        else:
            message = "Password cannot be empty"
        return Response({"detail": message}, status_code)
