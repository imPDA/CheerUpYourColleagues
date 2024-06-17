import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings

BASE_PATH = pathlib.Path(__file__).resolve().parent.parent  # app folder


class Config(BaseSettings):
    ms_teams_webhook: str = Field(alias='webhook')
    posting_interval: int = 60
    imgur_client_id: str = Field(alias='imgur_client_id')
    path_to_toad_links: pathlib.Path = (
        BASE_PATH / 'infra/repositories/picture/toad_memes.json'
    )
