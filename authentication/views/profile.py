from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.exceptions import InvalidUserException
from authentication.models import Profile
from authentication.serializers.profile import ProfileSerializer
from settings.utils.helpers import serializer_errors
import boto3


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Profile.objects.filter(user_id=request.user.id).first()
        serializer = ProfileSerializer(queryset, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request):
        instance = Profile.objects.filter(user_id=request.user.id).first()
        data = request.data
        #data["user_id"] = request.user.id
        object_name = request.data.get("file", "")
        if object_name:
            print ("entered in if")
            file_name = request.user.id
            s3 = boto3.client('s3', aws_access_key_id='AKIAQDQXUW4VV7HSLFXE',
                              aws_secret_access_key='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')
            bucket_path = 'octagon-user-profile-images'
            file_path = 'profile_images/' + str(file_name)
            s3.upload_fileobj(object_name.file, bucket_path, file_path,
                              ExtraArgs={'ContentEncoding': 'base64', 'ContentDisposition': 'inline',
                                         'ContentType': 'image/jpeg', 'StorageClass': "STANDARD_IA",
                                         'ACL': 'public-read'})
            file_url = "https://octagon-user-profile-images.s3.us-west-1.amazonaws.com/profile_images/" + str(file_name)
            instance.file_url = file_url
        if instance is None:
            print(instance)
            instance = Profile.objects.create(user_id=request.user.id)
        instance.company_id = request.user.profile.company_id
        serializer = ProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=data.get("company"))
            return Response({"detail": "Profile updated successfully"}, status=status.HTTP_200_OK)
        data = serializer_errors(serializer)
        raise InvalidUserException(data)

