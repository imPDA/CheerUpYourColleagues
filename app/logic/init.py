from functools import lru_cache

from punq import Container

from infra.message_senders.base import BaseMessageSender
from infra.message_senders.teams_webhook import TeamsWebhookMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.picture.lorem_picsum import LoremPicsumPictureRepository
from infra.repositories.quote.base import BaseQuoteRepository
from infra.repositories.quote.quotable_io import QuotableIOQuoteRepository
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    container = Container()

    # configs
    container.register(Config, instance=Config())
    config: Config = container.resolve(Config)

    # repos
    container.register(BasePictureRepository, instance=LoremPicsumPictureRepository())
    container.register(BaseQuoteRepository, instance=QuotableIOQuoteRepository())

    # senders
    container.register(BaseMessageSender, instance=TeamsWebhookMessageSender(
        config.teams_webhook_url
    ))

    return container
