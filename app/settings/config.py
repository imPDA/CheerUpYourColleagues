from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ms_teams_webhook: str = Field(alias='webhook')
    posting_interval: int = 60
    minio_endpoint: str = 'minio:9000'
    minio_access_key: str = Field(alias='minio_access_key')
    minio_secret_key: str = Field(alias='minio_secret_key')
    minio_bucket_name: str = 'pictures'
    database_connection_string: str = Field(alias='database_connection_string')
