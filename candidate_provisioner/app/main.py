from fastapi import FastAPI

from app.settings import settings
from app.clients import S3Client

app = FastAPI(title="FastAPI App", version="1.0")


@app.get("/")
def read_root():
    return {
        "message": "Okay!",
    }


@app.get("/presigned-url")
def generate_presigned_url():
    s3_client = S3Client(bucket_name=settings.aws.s3_bucket)
    url = s3_client.generate_presigned_url("example.pdf")
    return {"url": url}
