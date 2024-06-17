import logging
from datetime import datetime

from infra.message_senders.base import BaseMessageSender
from infra.repositories.picture.base import BasePictureRepository, PictureObject
from infra.repositories.statistics.base import BaseStatisticsRepository, QuoteObject
from infra.repositories.statistics.rdb_tables import QuoteRecord
from infra.sources.picture.base import BasePictureSource
from infra.sources.quote.base import BaseQuoteSource

from logic.init import init_container


def send_random_image_and_text():
    logging.getLogger('app').debug('`send_random_image_and_text` fired')

    container = init_container()

    picture_source = container.resolve(BasePictureSource)
    quotes_source = container.resolve(BaseQuoteSource)

    picture = picture_source.get_random()
    quote = quotes_source.get_random()

    statistics_repository: BaseStatisticsRepository = container.resolve(
        BaseStatisticsRepository
    )
    quote_was_already_sent = bool(
        statistics_repository.find(QuoteRecord.quote == quote.text)
    )
    if quote_was_already_sent:
        raise Exception('This quote was already sent before!')

    sender: BaseMessageSender = container.resolve(BaseMessageSender)
    sender.send(quote=quote.text, author=quote.author, image=picture.public_link)

    picture_repository: BasePictureRepository = container.resolve(BasePictureRepository)
    picture_object = PictureObject(obj=picture.obj, ext='jpeg')
    picture_repository.create(picture_object)

    quote_object = QuoteObject(
        quote=quote.text,
        author=quote.author,
        send_dt=int(datetime.now().timestamp()),
        picture_url=picture.public_link,
        picture_name=picture_object.name,
    )
    statistics_repository.create(quote_object)
