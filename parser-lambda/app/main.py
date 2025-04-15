from config import settings
from clients import S3Client, DynamoClient
from services import ResumeParser, DocIndexer

s3_client = S3Client()
dynamo_client = DynamoClient()
indexer = DocIndexer("test_index")


def handler(event, context):
    print("Event:", event)

    try:
        path = event.get("path")
        uid = path.split("/")[0]
        filename = path.split("/")[1]

        file_content = s3_client.get_file_content(path)

        parser = ResumeParser(file_content, path)
        parsed_content = parser.get_parsed_content()

        indexer.index_data(parsed_content, uid)

        dynamo_client.mark_completed(uid, filename)

        return {"statusCode": 200, "body": "test"}
    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"statusCode": 500, "body": str(e)}


handler({"path": "manmeetkohli1049@gmail.com/resume.pdf"}, None)
