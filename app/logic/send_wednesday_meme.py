import logging

from infra.message_senders.base import BaseMessageSender
from infra.sources.picture.wednesday import WednesdayPictureSource
from logic.init import init_container


def send_random_wednesday_meme():
    logging.getLogger('app').debug('`send_random_wednesday_meme` fired')

    container = init_container()

    wednesday_meme_repository: WednesdayPictureSource = container.resolve(
        WednesdayPictureSource
    )
    picture = wednesday_meme_repository.get_random()
    quote = "It's Wednesday, My Dudes!"

    sender = container.resolve(BaseMessageSender)
    sender.send(quote=quote, image=picture.public_link)


def get_wednesday_meme_picture_url():
    container = init_container()

    wednesday_meme_repository: WednesdayPictureSource = container.resolve(
        WednesdayPictureSource
    )

    return wednesday_meme_repository.get_random().public_link
