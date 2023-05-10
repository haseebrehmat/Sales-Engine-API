import uuid
from datetime import datetime

import boto3


def upload_image(object_name, user_id):
    file_name = str(user_id) + str(uuid.uuid4())
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


def upload_pdf(object_name, user_id):
    file_name = str(user_id) + str(uuid.uuid4())
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

    try:
        file = object_name.file
    except:
        file = object_name
    s3.upload_fileobj(file, bucket_path, file_path,
                      ExtraArgs={'ContentType': 'application/pdf',
                                 'ACL': 'public-read'})

    file_url = "https://d3mag5wsxt0rth.cloudfront.net/" + str(file_name)
    return file_url


def upload_csv(file_path, file_name):
    s3 = boto3.client('s3', aws_access_key_id='AKIAQDQXUW4VV7HSLFXE',
                      aws_secret_access_key='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')

    # Delete the Previous Image of User
    bucket_path = 'octagon-user-profile-images'
    s3.upload_file(file_path, bucket_path, file_name,
                      ExtraArgs={'ContentType': 'text/*',
                                 'ACL': 'public-read'})

    file_url = "https://d3mag5wsxt0rth.cloudfront.net/" + str(file_name)
    return file_url
