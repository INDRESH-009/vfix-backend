import boto3, json
from app.core.config import settings

session = boto3.session.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
)
s3 = session.client("s3", endpoint_url=settings.S3_ENDPOINT, verify=settings.S3_USE_SSL)

def ensure_bucket(name: str):
    try:
        s3.head_bucket(Bucket=name)
        print(f"Bucket exists: {name}")
    except Exception:
        s3.create_bucket(Bucket=name)
        print(f"Created bucket: {name}")
    policy = {
        "Version":"2012-10-17",
        "Statement":[{
            "Sid":"PublicRead",
            "Effect":"Allow",
            "Principal":"*",
            "Action":["s3:GetObject"],
            "Resource":[f"arn:aws:s3:::{name}/*"]
        }]
    }
    s3.put_bucket_policy(Bucket=name, Policy=json.dumps(policy))
    print("Set public-read policy")

if __name__ == "__main__":
    ensure_bucket(settings.S3_BUCKET)
    print("Done.")
