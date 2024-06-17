import logging

from infra.message_senders.base import BaseMessageSender
from infra.repositories.picture.wednesday import WednesdayPictureRepository

from logic.init import init_container


def send_random_wednesday_meme():
    logging.getLogger('app').debug('`send_random_wednesday_meme` fired')

    container = init_container()

    meme_repository: WednesdayPictureRepository = container.resolve(
        WednesdayPictureRepository
    )
    picture = meme_repository.get_random()
    quote = "It's Wednesday, My Dudes!"

    sender = container.resolve(BaseMessageSender)
    sender.send(quote=quote, image=picture.public_link)
