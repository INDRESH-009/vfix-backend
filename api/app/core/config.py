from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "DEV"
    APP_SECRET: str = "devsecret"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "civicdb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://localhost:6379/0"

    S3_ENDPOINT: str = "http://localhost:9000"
    S3_REGION: str = "us-east-1"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "civic-media"
    S3_USE_SSL: bool = False
    S3_PUBLIC_BASE: str = "http://localhost:9000/civic-media"

    OTP_CODE_DEV: str = "123456"
    OTP_TTL_SECONDS: int = 300

    class Config:
        env_file = ".env"

settings = Settings()
