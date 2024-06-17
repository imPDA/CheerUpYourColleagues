import logging

from infra.message_senders.base import BaseMessageSender
from infra.repositories.picture.base import BasePictureRepository
from infra.repositories.quote.base import BaseQuoteRepository

from logic.init import init_container


def send_random_image_and_text():
    logging.getLogger('app').debug('`send_random_image_and_text` fired')

    container = init_container()

    picture_repository = container.resolve(BasePictureRepository)
    quotes_repository = container.resolve(BaseQuoteRepository)

    picture = picture_repository.get_random()
    quote = quotes_repository.get_random()

    sender = container.resolve(BaseMessageSender)
    sender.send(quote=quote.text, author=quote.author, image=picture.public_link)


def get_random_image_url() -> str:
    container = init_container()

    picture_repository: BasePictureRepository = container.resolve(BasePictureRepository)
    picture = picture_repository.get_random()

    return picture.public_link


def get_random_quote() -> dict:
    container = init_container()

    quotes_repository: BaseQuoteRepository = container.resolve(BaseQuoteRepository)
    quote = quotes_repository.get_random()

    return quote.to_dict()


def send_image_and_quote_to_teams(quote: dict, image_url: str):
    container = init_container()

    sender: BaseMessageSender = container.resolve(BaseMessageSender)
    sender.send(quote=quote['text'], author=quote['author'], image=image_url)
