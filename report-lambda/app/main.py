# ---------- Endpoint for Lambda function ---------- #

from config import settings
from clients import S3Client


s3_client = S3Client()


def handler(event, context):
    print("Event:", event)

    s3_path = event["Records"][0]["s3"]["object"]["key"]
    file_content = s3_client.get_file_content(s3_path)

    return {"statusCode": 200, "body": "OKAY👍"}


###### what to expect in the event #######
# The event will contain the S3 bucket and object key that triggered the Lambda function.
# This s3 path is supposed to have the JD file that will be used to create the report.
# The event will look something like this:
# {
#     "Records": [
#         {
#             "s3": {
#                 "object": {
#                     "key": "new-object.txt",
#                     "size": 1024,
#                     "eTag": "d41d8cd98f00b204e9800998ecf8427e",
#                     "sequencer": "0A1B2C3D4E5F678901",
#                 },
#             }
#         }
#     ]
# }
