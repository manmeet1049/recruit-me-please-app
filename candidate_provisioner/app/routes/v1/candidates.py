from fastapi import APIRouter, HTTPException

from app.settings import settings
from app.clients import S3Client
from app.models import FileRequest

router = APIRouter(prefix="/candidate", tags=["Candidates"])


@router.post("/register")
def register(file_req: FileRequest):
    if not file_req.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    s3_client = S3Client(bucket_name=settings.aws.s3_bucket)
    print(file_req.filename)
    url = s3_client.generate_presigned_url(file_req.filename)
    return {"url": url}
