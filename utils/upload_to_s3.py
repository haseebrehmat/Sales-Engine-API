import os
import uuid
from datetime import datetime

import boto3
from settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def upload_image(object_name, user_id):
    file_name = str(user_id) + str(uuid.uuid4())
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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
    except Exception as e:
        file = object_name
    s3.upload_fileobj(file, bucket_path, file_path,
                      ExtraArgs={'ContentType': 'application/pdf',
                                 'ACL': 'public-read'})

    file_url = "https://d3mag5wsxt0rth.cloudfront.net/" + str(file_name)
    return file_url


def upload_csv(file_path, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket_path = 'octagon-user-profile-images'
    s3.upload_file(file_path, bucket_path, file_name,
                      ExtraArgs={'ContentType': '*',
                                 'ACL': 'public-read'})

    file_url = "https://octagon-user-profile-images.s3.us-west-1.amazonaws.com/" + str(file_name)
    remove_files()
    return file_url


def upload_job_files(file_path, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket_path = 'octagon-user-profile-images'
    s3.upload_file(file_path, bucket_path, file_name,
                   ExtraArgs={'ContentType': '*',
                              'ACL': 'public-read'})

    file_url = "https://octagon-user-profile-images.s3.us-west-1.amazonaws.com/" + str(file_name)
    print(file_url)
    return file_url


def remove_files():
    try:
        folder_path = 'job_portal'
        files = os.listdir(folder_path)

        # Loop through the files and remove each one
        for file_name in files:
            if ".csv" in file_name and "export" in file_name:
                file_path = os.path.join(folder_path, file_name)
                try:
                    os.remove(file_path)
                    print(f"Removed {file_path}")
                except Exception as e:
                    msg = f"Failed to remove {file_path}. Error: {str(e)}"
                    print(msg)
    except Exception as e:
        print(e)


def upload_file(file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket_path = 'octagon-user-profile-images'
    s3.upload_fileobj(file, bucket_path, file_name, ExtraArgs={'ACL': 'public-read'})
    file_url = "https://octagon-user-profile-images.s3.us-west-1.amazonaws.com/" + str(file_name)
    return file_url