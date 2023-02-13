# from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from authentication.models import User, PasswordChangeLogs, ResetPassword
#
#
# class PasswordReset(APIView):
#     permission_classes = (AllowAny, )
#
#     def post(self, request, code):
#         status_code = status.HTTP_406_NOT_ACCEPTABLE
#         password = request.data.get("new_password")
#         try:
#             reset_password = ResetPassword.objects.get(reset_code=request.data.get(code))
#             if reset_password.created_at
#             user = User.objects.get(pk=reset_password.user.pk)
#             user.set_password(password)
#             user.save()
#             PasswordChangeLogs.objects.create(user_id=request.user.pk, password=make_password(password))
#             message = "Password changed successfully"
#             status_code = status.HTTP_200_OK
#         except ResetPassword.DoesNotExist:
#             message = "Invalid reset code"
#
#         return Response(message, status_code)
#
