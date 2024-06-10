from functools import lru_cache

import sqlalchemy
from infra.message_senders.base import BaseMessageSender
from infra.message_senders.teams_webhook import TeamsWebhookMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.picture.minio import MinioPictureRepository
from infra.repositories.statistics.base import BaseStatisticsRepository
from infra.repositories.statistics.rdb import RDBStatisticsRepository
from infra.sources.picture.base import BasePictureSource
from infra.sources.picture.lorem_picsum import LoremPicsumPictureSource
from infra.sources.quote.base import BaseQuoteSource
from infra.sources.quote.quotable_io import QuotableIOQuoteSource
from minio import Minio
from punq import Container, Scope
from settings.config import Config
from sqlalchemy import create_engine


@lru_cache(1)
def init_container() -> Container:
    container = Container()

    # configs
    config = Config()
    container.register(Config, instance=config)

    # sources
    container.register(BasePictureSource, instance=LoremPicsumPictureSource())
    container.register(BaseQuoteSource, instance=QuotableIOQuoteSource())

    # senders
    container.register(
        BaseMessageSender, instance=TeamsWebhookMessageSender(config.ms_teams_webhook)
    )

    # repositories
    container.register(
        Minio,
        instance=Minio(
            config.minio_endpoint,
            config.minio_access_key,
            config.minio_secret_key,
            secure=False,
        ),
    )
    container.register(
        BasePictureRepository,
        factory=MinioPictureRepository,
        scope=Scope.singleton,
        bucket_name=config.minio_bucket_name,
    )

    container.register(
        sqlalchemy.Engine,
        factory=create_engine,
        scope=Scope.singleton,
        url=config.database_connection_string,
    )
    container.register(
        BaseStatisticsRepository,
        factory=RDBStatisticsRepository,
        scope=Scope.singleton,
    )

    return container
