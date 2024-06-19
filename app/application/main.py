from datetime import datetime

from logger.base import create_logger
from logic.send_random_message import send_random_image_and_text
from logic.send_wednesday_meme import send_random_wednesday_meme

if __name__ == '__main__':
    logger = create_logger('app')
    logger.info('Script called!')

    if datetime.now().weekday() == 2:
        send_random_wednesday_meme()
    else:
        send_random_image_and_text()
