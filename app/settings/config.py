from pydantic import BaseConfig, Field, AliasChoices


class Config(BaseConfig):
    ms_teams_webhook = Field(alias='webhook')
