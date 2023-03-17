from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Profile
import boto3


class ProfileViewImage(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        conditions = [
            request.data.get("file", "") != "",
            # request.data.get("employee_id", "") != ""
        ]
        if not all(conditions):
            return Response({"detail": "Fields cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = Profile.objects.filter(user_id=request.user.id).first()
        if instance is None:  # Incase Profile Doesn't exist
            instance = Profile.objects.create(user_id=request.user.id)

        image = request.data.get('file')
        valid_images = [
            'image/jpg',
            'image/jpeg',
            'image/png',
            'image/webp',
        ]
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        if image.content_type not in valid_images:
            message = "Image format is not valid, please choose JPG, JPEG, PNG or Webp"

        elif image.size > 4096000:    # 4096000 Bytes => 4 mbs
            message = "Image cannot be greater than 8mb"
        else:
            url = self.upload_image(object_name=image, user_id=request.user.id)
            instance.file_url = url
            instance.save()
            message = "Profile updated successfully"
            status_code = status.HTTP_200_OK

        return Response({"detail": message, "image_url": url}, status=status_code)

    def upload_image(self, object_name, user_id):
        file_name = str(user_id) + str(datetime.now())
        s3 = boto3.client('s3', aws_access_key_id='AKIAQDQXUW4VV7HSLFXE',
                          aws_secret_access_key='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')

        # Delete the Previous Image of User
        key_prefix = f"profile_images/{user_id}"
        response = s3.list_objects_v2(Bucket='octagon-user-profile-images', Prefix=key_prefix)
        for obj in response.get('Contents', []):
            s3.delete_object(Bucket='octagon-user-profile-images', Key=obj['Key'])

        # Upload updated image of User
        bucket_path = 'octagon-user-profile-images'
        file_path = 'profile_images/' + str(file_name)
        s3.upload_fileobj(object_name.file, bucket_path, file_path,
                          ExtraArgs={'ContentEncoding': 'base64', 'ContentDisposition': 'inline',
                                     'ContentType': 'image/jpeg', 'StorageClass': "STANDARD_IA",
                                     'ACL': 'public-read'})
        file_url = "https://d3mag5wsxt0rth.cloudfront.net/" + str(file_name)
        return file_url
