import json

import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from settings.utils.helpers import get_host


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
                User.objects.get(email=email)
                host = get_host(request)
                url = host + '/api/auth/authenticate/'
                headers = {
                    "Content-Type": "application/json"
                }
                payload = {
                    "email": email,
                    "password": password
                }
                resp = requests.post(
                    url,
                    data=json.dumps(payload),
                    headers=headers
                )
                status_code = resp.status_code
                if status_code == 500:
                    data = {"detail": "Something went wrong! Contact support"}
                elif status_code == 401:
                    data = {
                        "detail": 'Wrong password. Try again or click Forgot password to reset it.'
                    }
                else:
                    data = json.loads(resp.text)

            except User.DoesNotExist:
                data = {"detail": "User not found"}

        return Response(data, status_code)
