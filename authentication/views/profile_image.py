from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import Profile
from authentication.serializers.profile import ProfileSerializer
from settings.utils.helpers import serializer_errors
import boto3


class ProfileViewImage(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request):
        conditions = [
            request.data.get("file", "") != "",
            #request.data.get("employee_id", "") != ""
        ]
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = Profile.objects.filter(user_id=request.user.id).first()
        if instance is None:  # Incase Profile Doesn't exist
            instance = Profile.objects.create(user_id=request.user.id)
        serializer = ProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            url = self.upload_image(object_name=request.data.get('file'), user_id=request.user.id)
            serializer.save(file_url=url)
            return Response({"detail": "Profile updated successfully"}, status=status.HTTP_200_OK)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)
    def upload_image(self, object_name, user_id):
        file_name = user_id
        s3 = boto3.client('s3', aws_access_key_id='AKIAQDQXUW4VV7HSLFXE',
                          aws_secret_access_key='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')
        bucket_path = 'octagon-user-profile-images'
        file_path = 'profile_images/' + str(file_name)
        s3.upload_fileobj(object_name.file, bucket_path, file_path,
                          ExtraArgs={'ContentEncoding': 'base64', 'ContentDisposition': 'inline',
                                     'ContentType': 'image/jpeg', 'StorageClass': "STANDARD_IA",
                                     'ACL': 'public-read'})
        file_url = "https://octagon-user-profile-images.s3.us-west-1.amazonaws.com/profile_images/" + str(file_name)
        return file_url


