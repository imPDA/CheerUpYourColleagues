from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ms_teams_webhook: str = Field(alias='webhook')
