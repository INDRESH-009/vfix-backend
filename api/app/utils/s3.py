import boto3, uuid
from app.core.config import settings

session = boto3.session.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
)

s3 = session.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT,
    verify=settings.S3_USE_SSL,
)

def upload_bytes(content: bytes, content_type: str) -> str:
    key = f"media/{uuid.uuid4()}"
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=content, ContentType=content_type, ACL="public-read")
    return f"{settings.S3_PUBLIC_BASE}/{key}"
