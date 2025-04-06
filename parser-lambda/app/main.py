from config import settings
from clients import S3Client
from services import ResumeParser

s3_client = S3Client(settings.aws.s3_bucket)


def handler(event, context):
    print("Event:", event)
    
    file_name = event.get("path")
    file_content = s3_client.get_file_content(file_name)

    parser = ResumeParser(file_content, file_name)

    try:
        return {"statusCode": 200, "body": "test"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}


handler({"path": "example.pdf"}, None)
