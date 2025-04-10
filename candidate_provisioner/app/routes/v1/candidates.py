from fastapi import APIRouter, HTTPException

from app.settings import settings
from app.clients import S3Client, DynamoClient
from app.models import FileRequest

router = APIRouter(prefix="/candidate", tags=["Candidates"])


@router.post("/register")
def register(request: FileRequest):
    if not request.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    s3_client = S3Client(bucket_name=settings.aws.s3_bucket)
    url = s3_client.generate_presigned_url(f"{request.email}/{request.filename}")
    dynamo_client = DynamoClient(table_name=settings.aws.dynamo_table)
    dynamo_client.add_user(
        email=request.email,
        file_name=request.filename,
        phone=request.phone,
        name=request.name,
    )
    return {"url": url}
