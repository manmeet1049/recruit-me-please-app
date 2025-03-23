from fastapi import APIRouter

from app.settings import settings
from app.clients import S3Client

router = APIRouter(prefix="/candidate", tags=["Candidates"])


@router.get("/register")
def register():
    s3_client = S3Client(bucket_name=settings.aws.s3_bucket)
    url = s3_client.generate_presigned_url("example.pdf")
    return {"url": url}
