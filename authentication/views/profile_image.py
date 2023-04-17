from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import Profile
from utils.upload_to_s3 import upload_image


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
            url = upload_image(object_name=image, user_id=request.user.id)
            instance.file_url = url
            instance.save()
            message = "Profile updated successfully"
            status_code = status.HTTP_200_OK

        return Response({"detail": message, "image_url": url}, status=status_code)

