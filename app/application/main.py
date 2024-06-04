from logger.base import create_logger
from logic.send_random_message import send_random_image_and_text

if __name__ == '__main__':
    logger = create_logger('app')
    logger.info('Script called!')

    send_random_image_and_text()
