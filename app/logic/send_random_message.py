import logging

from infra.message_senders.base import BaseMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.quote.base import BaseQuoteRepository

from logic.init import init_container


async def send_random_image_and_text():
    logging.getLogger('app').debug('`send_random_image_and_text` fired')

    container = init_container()

    picture_repository = container.resolve(BasePictureRepository)
    quotes_repository = container.resolve(BaseQuoteRepository)

    picture = picture_repository.get_random()
    quote = quotes_repository.get_random()

    sender = container.resolve(BaseMessageSender)
    sender.send(text=str(quote), image=picture.public_link)
