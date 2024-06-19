from functools import lru_cache

import boto3
from botocore.client import Config as AWSConfig
from minio import Minio
from punq import Container, Scope
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from infra.message_senders.base import BaseMessageSender
from infra.message_senders.teams_webhook import TeamsWebhookMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.picture.s3 import S3_Client, S3PictureRepository
from infra.repositories.statistics.base import BaseStatisticsRepository
from infra.repositories.statistics.rdb import RDBStatisticsRepository
from infra.sources.picture.base import BasePictureSource
from infra.sources.picture.lorem_picsum import LoremPicsumPictureSource
from infra.sources.picture.wednesday import (
    ImgurWednesdayPictureSource,
    WednesdayPictureSource,
)
from infra.sources.quote.base import BaseQuoteSource
from infra.sources.quote.quotable_io import QuotableIOQuoteSource
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    container = Container()

    # configs
    config = Config()
    container.register(Config, instance=config)

    # sources
    container.register(BasePictureSource, instance=LoremPicsumPictureSource())
    container.register(BaseQuoteSource, instance=QuotableIOQuoteSource())
    container.register(
        WednesdayPictureSource,
        instance=ImgurWednesdayPictureSource(
            client_id=config.imgur_client_id,
            list_of_hashes=config.path_to_toad_links,
        ),
    )

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
    s3_client = boto3.client(
        's3',
        endpoint_url=config.timeweb_s3_endpoint_url,
        region_name=config.timeweb_s3_region_name,
        aws_access_key_id=config.timeweb_s3_access_key,
        aws_secret_access_key=config.timeweb_s3_secret_key,
        config=AWSConfig(s3={'addressing_style': 'path'}),
    )
    container.register(S3_Client, instance=s3_client)

    container.register(
        BasePictureRepository,
        factory=S3PictureRepository,
        scope=Scope.singleton,
        bucket_name=config.timeweb_s3_pictures_bucket_name,
    )

    container.register(
        Engine,
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
