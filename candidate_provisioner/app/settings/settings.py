# Description: This file contains the settings for the application. It uses pydantic_settings to load the settings from the .env file. The settings are loaded from the .env file automatically. If the .env file is not found, a warning message is printed. The settings are loaded based on the MODE environment variable. If the MODE environment variable is set to dev, the settings are loaded from the .dev.env file. If the MODE environment variable is set to prod, the settings are loaded from the .prod.env file. The settings are accessed using the settings object.
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv(".dev.env" if os.getenv("MODE", "dev") == "dev" else ".prod.env")

if ENV_FILE:
    load_dotenv(ENV_FILE)
else:
    print("Warning: No .env file found")


class DatabaseSettings(BaseSettings):
    url: str = os.getenv("DATABASE_URL")


class AWSSettings(BaseSettings):
    access_key: str = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    region: str = os.getenv("AWS_REGION")
    endpoint_url: str = os.getenv("ENDPOINT_URL")
    s3_bucket: str = os.getenv("S3_BUCKET")
    class Config:
        extra = "allow"


class Settings(BaseSettings):
    mode: str = os.getenv("MODE", "dev")
    secret_key: str = os.getenv("SECRET_KEY")

    database: DatabaseSettings = DatabaseSettings()
    aws: AWSSettings = AWSSettings()

    class Config:
        env_file = ENV_FILE
        extra = "allow"


settings = Settings()
