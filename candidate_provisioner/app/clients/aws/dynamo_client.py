import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from app.settings.settings import settings


class DynamoClient:
    def __init__(self, table_name):
        self.table_name = table_name

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=settings.aws.region,
            endpoint_url=settings.aws.endpoint_url,
            aws_access_key_id=settings.aws.access_key,
            aws_secret_access_key=settings.aws.secret_key,
        )

        self.table = self._ensure_table()

    def _ensure_table(self):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.load()
            print(f"✅ Table '{self.table_name}' exists.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                print(f"⚠️ Table '{self.table_name}' does not exist. Creating it...")
                table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {"AttributeName": "PK", "KeyType": "HASH"},
                        {"AttributeName": "SK", "KeyType": "RANGE"},
                    ],
                    AttributeDefinitions=[
                        {"AttributeName": "PK", "AttributeType": "S"},
                        {"AttributeName": "SK", "AttributeType": "S"},
                        {
                            "AttributeName": "s3_path",
                            "AttributeType": "S",
                        },  # GSI index key
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            "IndexName": "S3PathIndex",
                            "KeySchema": [
                                {"AttributeName": "s3_path", "KeyType": "HASH"},
                            ],
                            "Projection": {"ProjectionType": "ALL"},
                        }
                    ],
                    BillingMode="PAY_PER_REQUEST",
                )

                table.wait_until_exists()
                print("✅ Table created.")
            else:
                raise
        return table

    def add_user(self, email, file_name, phone, name, status="PENDING"):
        now = datetime.utcnow()
        expiry = now + timedelta(days=30)
        s3_path = f"{email}/{file_name}"

        item = {
            "PK": f"USER#{email}",
            "SK": f"RESUME#{file_name}",
            "email": email,
            "file_name": file_name,
            "phone": phone,
            "name": name,
            "upload_date": now.isoformat(),
            "expiry_date": expiry.isoformat(),
            "s3_path": s3_path,
            "status": status,
        }

        self.table.put_item(Item=item)
        print(f"✅ Resume entry added for {email} - {file_name}")
        return item
