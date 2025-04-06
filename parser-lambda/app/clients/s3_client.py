import boto3
from botocore.exceptions import (
    BotoCoreError,
    NoCredentialsError,
    PartialCredentialsError,
)

from config import settings


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

    def get_file_content(self, object_key: str):
        """Fetch and return the file content from the S3 bucket."""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=object_key
            )
            content = response["Body"].read()
            return content
        except self.s3_client.exceptions.NoSuchKey:
            print(f"File not found: {object_key}")
            return None
        except (BotoCoreError, NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error fetching file from S3: {e}")
            return None
