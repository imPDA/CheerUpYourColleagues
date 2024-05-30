import asyncio

import logging
import signal
from datetime import datetime, timedelta

from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.triggers.interval import IntervalTrigger

from infra.message_senders.teams_webhook import TeamsWebhookMessageSender
from infra.repositories.picture.lorem_picsum import LoremPicsumPictureRepository
from infra.repositories.quote.quotable_io import QuotableIOQuoteRepository
from logger.base import create_logger


async def send_random_image_and_text():
    logger = logging.getLogger('app')
    logger.debug('Task fired')

    picture_repository = LoremPicsumPictureRepository()
    quotes_repository = QuotableIOQuoteRepository()

    picture = picture_repository.get('/320')
    quote = quotes_repository.get_random()

    sender = TeamsWebhookMessageSender("https://<webhook here>")
    sender.send(text=str(quote), image=picture.public_link)


def error_listener(event: JobExecutionEvent) -> None:
    logging.getLogger('app').exception("Job raised an exception", exc_info=event.exception)


if __name__ == '__main__':
    logger = create_logger('app')
    logging.getLogger('apscheduler.executors.default').disabled = True

    loop = asyncio.new_event_loop()

    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_listener(error_listener, EVENT_JOB_ERROR)

    trigger = IntervalTrigger(minutes=60)
    job = scheduler.add_job(send_random_image_and_text, trigger)

    def graceful_stop():
        logger.info('Stopping scheduler...')
        scheduler.shutdown(wait=False)
        logger.info('Sheduler shutted down!')

    loop.add_signal_handler(signal.SIGTERM, graceful_stop)

    scheduler.start()

    # next run scheduled at `now() + interval` by default, but I want it
    # fire right after the loop started, so let's adjust `next_run_time`
    job.modify(next_run_time=datetime.now() + timedelta(seconds=1))

    try:
        logger.info('App started!')
        loop.run_forever()
    finally:
        loop.close()
