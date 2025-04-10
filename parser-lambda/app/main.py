from config import settings
from clients import S3Client
from services import ResumeParser, DocIndexer

s3_client = S3Client(settings.aws.s3_bucket)
indexer = DocIndexer("test_index")


def handler(event, context):
    print("Event:", event)

    try:
        file_name = event.get("path")
        uid = file_name.split("/")[0]

        file_content = s3_client.get_file_content(file_name)

        parser = ResumeParser(file_content, file_name)
        parsed_content = parser.get_parsed_content()
        # print("Parsed Content:", parsed_content)

        indexer.index_data(parsed_content, uid)

        return {"statusCode": 200, "body": "test"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"statusCode": 500, "body": str(e)}


handler({"path": "manmeetkohli1049@gmail.com/resume.docx"}, None)
