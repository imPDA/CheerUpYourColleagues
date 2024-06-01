import asyncio
import functools
import logging
import signal
from datetime import datetime, timedelta

from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.interval import IntervalTrigger
from logger.base import create_logger
from logic.init import init_container
from logic.send_random_message import send_random_image_and_text
from settings.config import Config


def error_listener(event: JobExecutionEvent) -> None:
    logging.getLogger('app').exception(
        'Job raised an exception', exc_info=event.exception
    )


def graceful_stop(scheduler: BaseScheduler):
    logger = logging.getLogger('app')
    logger.info('Stopping scheduler...')
    scheduler.shutdown(wait=False)
    logger.info('Sheduler shutted down!')


if __name__ == '__main__':
    logger = create_logger('app')
    logging.getLogger('apscheduler.executors.default').disabled = True

    container = init_container()
    config: Config = container.resolve(Config)

    loop = asyncio.new_event_loop()

    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_listener(error_listener, EVENT_JOB_ERROR)

    trigger = IntervalTrigger(minutes=config.posting_interval)
    job = scheduler.add_job(send_random_image_and_text, trigger)

    loop.add_signal_handler(signal.SIGTERM, functools.partial(graceful_stop, scheduler))
    # TODO: would be fine to add uvicorn style of handling signals

    scheduler.start()

    # next run scheduled at `now() + interval` by default, but I want it
    # fire right after the loop started, so let's adjust `next_run_time`
    job.modify(next_run_time=datetime.now() + timedelta(seconds=1))

    try:
        logger.info('App started!')
        loop.run_forever()
    finally:
        loop.close()
