import json
import requests
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from authentication.views.users import LoginView
from settings.utils.helpers import get_host
from django.test import RequestFactory


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        status_code = status.HTTP_401_UNAUTHORIZED
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        if email == "" or password == "":
            data = {"detail": "Credentials cannot not be empty"}
        else:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    return Response({"detail": "User is no longer active, Contact Admin"}, status.HTTP_401_UNAUTHORIZED)

                headers = {
                    "Content-Type": "application/json"
                }
                payload = {
                    "email": email,
                    "password": password
                }
                request_factory = RequestFactory()
                drf_request = request_factory.post('/api/auth/authenticate/', data=payload, headers=headers)
                drf_request.method = "POST"
                view = LoginView.as_view()
                resp = view(drf_request)
                status_code = resp.status_code
                if status_code == 500:
                    data = {"detail": "Something went wrong! Contact support"}
                elif status_code == 401:
                    data = {
                        "detail": 'Wrong password. Try again or click Forgot password to reset it.'
                    }
                else:
                    data = resp.data

            except User.DoesNotExist:
                data = {"detail": "User not found"}

        return Response(data, status_code)
