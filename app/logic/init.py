from functools import lru_cache

from infra.message_senders.base import BaseMessageSender
from infra.message_senders.teams_webhook import TeamsWebhookMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.picture.lorem_picsum import LoremPicsumPictureRepository
from infra.repositories.picture.wednesday import (
    ImgurWednesdayPictureRepository,
    WednesdayPictureRepository,
)
from infra.repositories.quote.base import BaseQuoteRepository
from infra.repositories.quote.quotable_io import QuotableIOQuoteRepository
from punq import Container
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    container = Container()

    # configs
    config = Config()
    container.register(Config, instance=config)

    # repos
    container.register(BasePictureRepository, instance=LoremPicsumPictureRepository())
    container.register(BaseQuoteRepository, instance=QuotableIOQuoteRepository())
    container.register(
        WednesdayPictureRepository,
        instance=ImgurWednesdayPictureRepository(
            client_id=config.imgur_client_id,
            list_of_hashes=config.path_to_toad_links,
        ),
    )

    # senders
    container.register(
        BaseMessageSender, instance=TeamsWebhookMessageSender(config.ms_teams_webhook)
    )

    return container
