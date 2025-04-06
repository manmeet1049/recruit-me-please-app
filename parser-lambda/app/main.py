from config import settings
from clients import S3Client

s3_client = S3Client(settings.aws.s3_bucket)


def handler(event, context):
    print("Event:", event)
    print(s3_client.get_file_content("example.pdf"))
    try:
        return {"statusCode": 200, "body": "test"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}


handler({"path": "s3-path"}, None)
