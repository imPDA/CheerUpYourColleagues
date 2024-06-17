import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent  # app folder


class Config(BaseSettings):
    ms_teams_webhook: str = Field(alias='webhook')
    posting_interval: int = 60
    minio_endpoint: str = 'minio:9000'
    minio_access_key: str = Field(alias='minio_access_key')
    minio_secret_key: str = Field(alias='minio_secret_key')
    minio_bucket_name: str = 'pictures'
    database_connection_string: str = Field(alias='database_connection_string')
    imgur_client_id: str = Field(alias='imgur_client_id')
    path_to_toad_links: pathlib.Path = (
        BASE_PATH / 'infra/repositories/picture/toad_memes.json'
    )
