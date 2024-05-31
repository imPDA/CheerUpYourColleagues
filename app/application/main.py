import asyncio

import logging
import signal
from datetime import datetime, timedelta

from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.triggers.interval import IntervalTrigger

from logger.base import create_logger
from logic.send_random_message import send_random_image_and_text


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

    loop.add_signal_handler(signal.SIGINT, graceful_stop)
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
