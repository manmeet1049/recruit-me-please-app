import boto3
from botocore.exceptions import (
    BotoCoreError,
    NoCredentialsError,
    PartialCredentialsError,
)

from app.settings.settings import settings


class S3Client:
    def __init__(self, bucket_name):
        """Initialize the S3 client with the specified bucket name."""
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.aws.region,
            aws_access_key_id=settings.aws.access_key,
            aws_secret_access_key=settings.aws.secret_key,
            endpoint_url=settings.aws.endpoint_url,
        )
        self.bucket_name = bucket_name

    def generate_presigned_url(self, object_name, expiration=3600):
        """Generate a pre-signed URL for uploading a PDF file."""
        try:
            # if not object_name.lower().endswith(".pdf"):
            #     raise ValueError("Only PDF files are allowed")

            response = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": object_name,
                    "ContentType": "application/pdf",
                },
                ExpiresIn=expiration,
            )
            return response
        except (BotoCoreError, NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error generating pre-signed URL: {e}")
            return None
        except ValueError as ve:
            print(f"Invalid file type: {ve}")
            return None
