from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings
from django.http import JsonResponse
import uuid

def generate_field_name(field):
    name = field.name

    if name.find('_') == -1:
        return name.capitalize()
    else:
        split_name = name.split('_')
        new_name = ' '.join(word.title() for word in split_name)
        return new_name


def generate_column(model, actions=True, default_fields=None):
    """
        Function to create list of fields in any table
    """

    fields = model._meta.fields

    columns = []

    for dbfield in fields:
        if dbfield.name in default_fields:
            columns.append({
                "value": dbfield.name,
                "text": dbfield.verbose_name if dbfield.verbose_name else generate_field_name(dbfield),
                "is_default": True
            })

        else:
            columns.append({
                "value": dbfield.name,
                "text": dbfield.verbose_name if dbfield.verbose_name else generate_field_name(dbfield),
                "is_default": False
            })

    if actions:
        columns.append({
            "value": 'actions',
            "text": 'Actions',
            "is_default": True
        })

    return columns


def compress_image(pic):
    """
        Function to compress the image to make thumb nile image
    """
    im = Image.open(pic)
    if im.mode == 'RGBA':
        im = im.convert('RGB')

    # Perform compression operations here
    image_io = BytesIO()
    im.save(image_io, format='JPEG', quality=40)  # Adjust quality as needed
    content_file = ContentFile(image_io.getvalue())

    return content_file

def upload_image_to_wasabi(file):
    """
    Uploads an image file to Wasabi and returns the generated object key.

    :param file: The file object received in the request.
    :return: Dictionary containing success status and object key or error message.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Generate a unique object key
    key = f"uploads/{uuid.uuid4()}_{file.name}"

    try:
        # Upload the file to Wasabi
        s3_client.upload_fileobj(
            Fileobj=file,
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=key
        )

        return {
        'success': True,
        'key': key
        }

    except Exception as e:
        return {
            'success': False,
            'error': f"Error uploading file: {str(e)}"
        }
    
def generate_presigned_url(object_key, expiration=3600):
    """
    Generates a pre-signed URL to access a file in Wasabi.

    :param object_key: The key of the file in the Wasabi bucket.
    :param expiration: The expiration time of the URL in seconds (default is 1 hour).
    :return: Dictionary containing success status and the pre-signed URL or error message.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        # Generate the pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': object_key
            },
            ExpiresIn=expiration
        )

        return {
            'success': True,
            'url': presigned_url
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error generating pre-signed URL: {str(e)}"
        }