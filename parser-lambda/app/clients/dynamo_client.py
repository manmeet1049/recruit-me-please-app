import boto3
from botocore.exceptions import ClientError
from datetime import datetime

from config import settings


class DynamoClient:
    def __init__(self):
        self.table_name = settings.aws.dyanmo_table

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=settings.aws.region,
            endpoint_url=settings.aws.endpoint_url,
            aws_access_key_id=settings.aws.access_key,
            aws_secret_access_key=settings.aws.secret_key,
        )

        self.table = self.dynamodb.Table(self.table_name)

    def mark_completed(self, email, file_name):
        pk = f"USER#{email}"
        sk = f"RESUME#{file_name}"

        try:
            now = datetime.utcnow().isoformat()

            response = self.table.update_item(
                Key={"PK": pk, "SK": sk},
                UpdateExpression="SET #s = :status, updated_at = :updated_at",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={
                    ":status": "COMPLETED",
                    ":updated_at": now,
                },
                ReturnValues="UPDATED_NEW",
            )
            print(f"✅ Marked COMPLETED for {email} - {file_name}")
            return response
        except ClientError as e:
            print(f"❌ Error updating status for {email} - {file_name}: {e}")
            return None

    def get_user_resume(self, email, file_name):
        pk = f"USER#{email}"
        sk = f"RESUME#{file_name}"

        try:
            response = self.table.get_item(Key={"PK": pk, "SK": sk})
            item = response.get("Item")
            if item:
                print(f"📄 Retrieved item for {email} - {file_name}")
            else:
                print(f"⚠️ No item found for {email} - {file_name}")
            return item
        except ClientError as e:
            print(f"❌ Error fetching item: {e}")
            return None
