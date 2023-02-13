import json

import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        status_code = status.HTTP_401_UNAUTHORIZED
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        if email == "" or password == "":
            data = "Credentials cannot not be empty"
        else:
            try:
                # User.objects.get(email=email)
                host = request.get_host()
                if 'http' not in host:
                    host = 'http://' + host
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
                    data = "Something went wrong! Contact support"
                else:
                    data = json.loads(resp.text)

            except User.DoesNotExist:
                data = "Email doesn't exist"

        return Response(data, status_code)
